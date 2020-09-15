select if(
(
  select count(1)
  from `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.errors` as errors
) = 0, 1,
cast((select 'Errors table is not empty') as INT64))