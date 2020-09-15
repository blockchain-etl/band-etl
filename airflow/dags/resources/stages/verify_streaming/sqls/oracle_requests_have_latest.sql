select if(
(
select timestamp_diff(
  current_timestamp(),
  (select max(block_timestamp_truncated)
  from `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.oracle_requests` as oracle_requests
  where date(block_timestamp_truncated) >= date_add('{{ds}}', INTERVAL -1 DAY)),
  MINUTE)
) < {{params.max_lag_in_minutes}}, 1,
cast((select 'Oracle requests are lagging by more than {{params.max_lag_in_minutes}} minutes') as INT64))
