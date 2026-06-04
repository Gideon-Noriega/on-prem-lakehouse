{{ config(materialized='view') }}

SELECT
    id,
    name AS symbol,
    created_at AS traded_at
FROM iceberg.demo.test_table
