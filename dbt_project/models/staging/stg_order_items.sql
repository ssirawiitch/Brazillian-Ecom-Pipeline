with raw_items as (
    select * from {{ source('olist_raw', 'order items') }}
)

select
    order_id,
    order_item_id as item_sequence, 
    product_id,
    seller_id,
    price,
    freight_value as shipping_cost,
    (price + freight_value) as total_item_price 
from raw_items