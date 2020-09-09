from __future__ import print_function

import logging
import os
from datetime import datetime, timedelta

from airflow import models
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectSensor
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from google.cloud import bigquery
from google.cloud.bigquery import TimePartitioning

from bandetl_airflow.bigquery_utils import submit_bigquery_job, create_dataset, read_bigquery_schema_from_file, \
    does_table_exist
from bandetl_airflow.file_utils import read_file

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def build_load_dag(
        dag_id,
        output_bucket,
        destination_dataset_project_id,
        chain='band',
        notification_emails=None,
        success_notification_emails=None,
        load_start_date=datetime(2018, 6, 30),
        load_end_date=None,
        load_schedule_interval='0 0 * * *',
        load_all_partitions=None
):
    """Build Load DAG"""

    dataset_name = f'crypto_{chain}'
    dataset_name_temp = f'crypto_{chain}_temp'

    if not destination_dataset_project_id:
        raise ValueError('destination_dataset_project_id is required')

    default_dag_args = {
        'depends_on_past': False,
        'start_date': load_start_date,
        'end_date': load_end_date,
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 5,
        'retry_delay': timedelta(minutes=5)
    }

    if notification_emails and len(notification_emails) > 0:
        default_dag_args['email'] = [email.strip() for email in notification_emails.split(',')]

    environment = {
        'dataset_name': dataset_name,
        'destination_dataset_project_id': destination_dataset_project_id
    }

    # Define a DAG (directed acyclic graph) of tasks.
    dag = models.DAG(
        dag_id,
        catchup=False if load_end_date is None else True,
        schedule_interval=load_schedule_interval,
        default_args=default_dag_args)

    dags_folder = os.environ.get('DAGS_FOLDER', '/home/airflow/gcs/dags')

    def add_load_tasks(task, time_partitioning_field='block_timestamp_truncated'):
        wait_sensor = GoogleCloudStorageObjectSensor(
            task_id='wait_latest_{task}'.format(task=task),
            timeout=60 * 60,
            poke_interval=60,
            bucket=output_bucket,
            object='export/{task}/block_date={datestamp}/{task}.json'.format(task=task, datestamp='{{ds}}'),
            dag=dag
        )

        def load_task():
            client = bigquery.Client()
            job_config = bigquery.LoadJobConfig()
            schema_path = os.path.join(dags_folder, 'resources/stages/load/schemas/{task}.json'.format(task=task))
            job_config.schema = read_bigquery_schema_from_file(schema_path)
            job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            job_config.write_disposition = 'WRITE_TRUNCATE'
            job_config.ignore_unknown_values = True
            job_config.time_partitioning = TimePartitioning(field=time_partitioning_field)

            export_location_uri = 'gs://{bucket}/export'.format(bucket=output_bucket)
            uri = '{export_location_uri}/{task}/*.json'.format(export_location_uri=export_location_uri, task=task)
            table_ref = create_dataset(client, dataset_name_temp).table(task)
            load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
            submit_bigquery_job(load_job, job_config)
            assert load_job.state == 'DONE'

        load_operator = PythonOperator(
            task_id='load_{task}'.format(task=task),
            python_callable=load_task,
            execution_timeout=timedelta(minutes=30),
            dag=dag
        )

        wait_sensor >> load_operator
        return load_operator

    def add_merge_tasks(task, dependencies=None):
        def merge_task(ds, **kwargs):
            client = bigquery.Client()

            dataset = create_dataset(client, dataset_name, project=destination_dataset_project_id)

            load_all_partitions_for_table = load_all_partitions
            if load_all_partitions_for_table is None:
                table_ref = dataset.table(task)
                table_exists = does_table_exist(client, table_ref)
                load_all_partitions_for_table = not table_exists
                logging.info('load_all_partitions for table {} is set to {}'.format(task, str(load_all_partitions_for_table)))

            if load_all_partitions_for_table:
                # Copy temporary table to destination
                copy_job_config = bigquery.CopyJobConfig()
                copy_job_config.write_disposition = 'WRITE_TRUNCATE'
                dest_table_ref = dataset.table(task)
                temp_table_ref = client.dataset(dataset_name_temp).table(task)
                copy_job = client.copy_table(temp_table_ref, dest_table_ref, location='US', job_config=copy_job_config)
                submit_bigquery_job(copy_job, copy_job_config)
                assert copy_job.state == 'DONE'
            else:
                merge_job_config = bigquery.QueryJobConfig()
                # Finishes faster, query limit for concurrent interactive queries is 50
                merge_job_config.priority = bigquery.QueryPriority.INTERACTIVE

                merge_sql_path = os.path.join(
                    dags_folder, 'resources/stages/load/sqls/merge.sql'.format(task=task))
                merge_sql_template = read_file(merge_sql_path)

                schema_path = os.path.join(dags_folder, 'resources/stages/load/schemas/{task}.json'.format(task=task))
                schema = read_bigquery_schema_from_file(schema_path)

                merge_template_context = {
                    'ds': ds,
                    'table': task,
                    'destination_dataset_project_id': destination_dataset_project_id,
                    'destination_dataset_name': dataset_name,
                    'dataset_name_temp': dataset_name_temp,
                    'table_schema': schema
                }

                merge_sql = kwargs['task'].render_template('', merge_sql_template, merge_template_context)
                print('Merge sql:')
                print(merge_sql)
                merge_job = client.query(merge_sql, location='US', job_config=merge_job_config)
                submit_bigquery_job(merge_job, merge_job_config)
                assert merge_job.state == 'DONE'

        merge_operator = PythonOperator(
            task_id='merge_{task}'.format(task=task),
            python_callable=merge_task,
            provide_context=True,
            execution_timeout=timedelta(minutes=60),
            dag=dag
        )

        if dependencies is not None and len(dependencies) > 0:
            for dependency in dependencies:
                dependency >> merge_operator
        return merge_operator

    def add_verify_tasks(task, dependencies=None):
        # The queries in verify/sqls will fail when the condition is not met
        # Have to use this trick since the Python 2 version of BigQueryCheckOperator doesn't support standard SQL
        # and legacy SQL can't be used to query partitioned tables.
        sql_path = os.path.join(dags_folder, 'resources/stages/verify/sqls/{task}.sql'.format(task=task))
        sql = read_file(sql_path)
        verify_task = BigQueryOperator(
            task_id='verify_{task}'.format(task=task),
            bql=sql,
            params=environment,
            use_legacy_sql=False,
            dag=dag)
        if dependencies is not None and len(dependencies) > 0:
            for dependency in dependencies:
                dependency >> verify_task
        return verify_task

    load_blocks_task = add_load_tasks('blocks')
    load_transactions_task = add_load_tasks('transactions')
    load_messages_task = add_load_tasks('messages')
    load_logs_task = add_load_tasks('logs')
    load_block_events_task = add_load_tasks('block_events')
    load_oracle_requests_task = add_load_tasks('oracle_requests')

    merge_blocks_task = add_merge_tasks('blocks', dependencies=[load_blocks_task])
    merge_transactions_task = add_merge_tasks('transactions', dependencies=[load_transactions_task])
    merge_messages_task = add_merge_tasks('messages', dependencies=[load_messages_task])
    merge_logs_task = add_merge_tasks('logs', dependencies=[load_logs_task])
    merge_block_events_task = add_merge_tasks('block_events', dependencies=[load_block_events_task])
    merge_oracle_requests_task = add_merge_tasks('oracle_requests', dependencies=[load_oracle_requests_task])

    if success_notification_emails and len(success_notification_emails) > 0:
        send_email_task = EmailOperator(
            task_id='send_email',
            to=[email.strip() for email in success_notification_emails.split(',')],
            subject='Band ETL Airflow Load DAG Succeeded',
            html_content='Band ETL Airflow Load DAG Succeeded - {}'.format(chain),
            dag=dag
        )

        merge_oracle_requests_task >> send_email_task

    return dag
