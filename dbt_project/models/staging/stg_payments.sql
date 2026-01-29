with raw_payments as (
    select * from {{ source('olist_raw', 'order payments') }}
)

select
    order_id,
    payment_type,
    payment_installments,
    payment_value
from raw_payments