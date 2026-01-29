with orders as (
    select * from {{ ref('stg_orders') }}
),
order_items as (
    select 
        order_id,
        sum(price) as total_revenue,
        sum(shipping_cost) as total_shipping_cost,
        count(item_sequence) as total_items
    from {{ ref('stg_order_items') }}
    group by 1
),
payments as (
    select 
        order_id,
        sum(payment_value) as total_paid_value
    from {{ ref('stg_payments') }}
    group by 1
)

select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchased_at,
    i.total_items,
    i.total_revenue,
    i.total_shipping_cost,
    p.total_paid_value,
    datetime_diff(o.delivered_customer_at, o.purchased_at, DAY) as delivery_time_days
from orders o
left join order_items i on o.order_id = i.order_id
left join payments p on o.order_id = p.order_id