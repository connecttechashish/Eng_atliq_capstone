{{ config(
    materialized='table',
    location='abfss://gold@atliqdatalake.dfs.core.windows.net/',
    schema='gold'
) }}

SELECT
    product_id,
    product_name,
    category,
    unit_price,
    updated_at,
    ingest_date,
    silver_loaded_at
FROM {{ source('atliq_silver', 'products') }}
