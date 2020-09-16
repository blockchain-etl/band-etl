select if(
(
  select count(*) - (max(block_height) - min(block_height) + 1)
  from `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.blocks` as blocks
  where date(block_timestamp_truncated) >= date_add('{{ds}}', INTERVAL -1 DAY)
) between -2 and 2, 1,
cast((select 'There are more than 2 missing or duplicate blocks') as INT64))
