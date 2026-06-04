{{ config(materialized='table') }}

SELECT
    symbol,
    COUNT(*) AS trade_count,
    MIN(traded_at) AS first_trade,
    MAX(traded_at) AS last_trade
FROM {{ ref('stg_trades') }}
GROUP BY symbol
