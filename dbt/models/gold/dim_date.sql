{{ config(
    materialized='table',
    schema='gold',
    location='abfss://gold@atliqdatalake.dfs.core.windows.net/'
) }}

WITH calendar AS (
    SELECT
        CAST(date AS DATE) AS date_day,
        YEAR(date) AS year,
        MONTH(date) AS month,
        DAY(date) AS day,
        WEEKOFYEAR(date) AS week_of_year,
        QUARTER(date) AS quarter
    FROM (
        SELECT explode(sequence(
            to_date('2025-01-01'),
            to_date('2026-12-31'),
            interval 1 day
        )) AS date
    )
)

SELECT * FROM calendar
