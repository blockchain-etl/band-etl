#standardSQL
SELECT
    DATE(block_timestamp_truncated) AS date,
    COUNT(DISTINCT sender) AS active_addresses
FROM `public-data-finance.crypto_band.transactions`
GROUP BY date
ORDER BY date DESC