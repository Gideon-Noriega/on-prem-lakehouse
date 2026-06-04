
  create or replace view
    "iceberg"."analytics"."stg_trades"
  security definer
  as
    

SELECT
    id,
    name AS symbol,
    created_at AS traded_at
FROM iceberg.demo.test_table
  ;
