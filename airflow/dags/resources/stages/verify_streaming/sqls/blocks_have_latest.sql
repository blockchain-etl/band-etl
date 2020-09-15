select if(
(
select timestamp_diff(
  current_timestamp(),
  (select max(block_timestamp_truncated)
  from `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.blocks` as blocks
  where date(block_timestamp_truncated) >= date_add('{{ds}}', INTERVAL -1 DAY)),
  MINUTE)
) < {{params.max_lag_in_minutes}}, 1,
cast((select 'Blocks are lagging by more than {{params.max_lag_in_minutes}} minutes') as INT64))
