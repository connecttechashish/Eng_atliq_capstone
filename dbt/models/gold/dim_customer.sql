{{ config(
    materialized='table',
    location='abfss://gold@atliqdatalake.dfs.core.windows.net/',
    schema='gold'
) }}


SELECT
    customer_id,
    customer_name,
    email,
    city,
    signup_date,
    updated_at,
    ingest_date,
    silver_loaded_at
FROM {{ source('atliq_silver', 'customers') }}
