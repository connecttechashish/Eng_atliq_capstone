{{ config(
    materialized='table',
    schema='gold'
) }}

SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.updated_at AS order_updated_at,
    o.silver_loaded_at AS order_silver_loaded_at,

    oi.order_item_id,
    oi.product_id,
    oi.quantity,
    oi.created_at AS item_created_at,
    oi.silver_loaded_at AS item_silver_loaded_at,

    p.payment_id,
    p.amount,
    p.method,
    p.paid_at,
    p.updated_at AS payment_updated_at,
    p.ingest_date AS payment_ingest_date,
    p.silver_loaded_at AS payment_silver_loaded_at,

    -- FINAL FIX: use dp.unit_price from dim_products
    (oi.quantity * dp.unit_price) AS line_total

FROM {{ source('atliq_silver', 'orders') }} o
LEFT JOIN {{ source('atliq_silver', 'order_items') }} oi
    ON o.order_id = oi.order_id
LEFT JOIN {{ source('atliq_silver', 'payments') }} p
    ON o.order_id = p.order_id
LEFT JOIN {{ ref('dim_product') }} dp
    ON oi.product_id = dp.product_id
