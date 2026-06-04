
  
    

    create table "iceberg"."analytics"."trade_summary"
      
      
    as (
      

SELECT
    symbol,
    COUNT(*) AS trade_count,
    MIN(traded_at) AS first_trade,
    MAX(traded_at) AS last_trade
FROM "iceberg"."analytics"."stg_trades"
GROUP BY symbol
    );

  