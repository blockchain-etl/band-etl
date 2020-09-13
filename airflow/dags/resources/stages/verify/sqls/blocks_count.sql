SELECT IF(
(
    SELECT MAX(block_height)
    FROM `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.blocks`
    WHERE DATE(block_timestamp_truncated) <= '{{ds}}'
) =
(
    SELECT COUNT(*) FROM `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.blocks`
    WHERE DATE(block_timestamp_truncated) <= '{{ds}}'
), 1,
CAST((SELECT 'Total number of blocks is not equal to last block number {{ds}}') AS INT64))
