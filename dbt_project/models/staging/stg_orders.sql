select
    order_id,
    customer_id,
    order_status,
    cast(order_purchase_timestamp as datetime) as purchased_at,
    cast(order_delivered_customer_date as datetime) as delivered_at
from {{ source('olist_raw', 'orders') }}