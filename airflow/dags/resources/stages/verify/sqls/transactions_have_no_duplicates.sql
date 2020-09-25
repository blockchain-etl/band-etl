SELECT IF(
(
    WITH duplicate_transactions AS (
        SELECT txhash, COUNT(*) AS count
        FROM `{{params.destination_dataset_project_id}}.{{params.dataset_name}}.transactions`
        GROUP BY txhash
        HAVING count > 1
    )
    SELECT COUNT(*)
    FROM duplicate_transactions
) = 0, 1,
CAST((SELECT 'There are duplicate transactions') AS INT64))
