select
    customer_id,
    customer_unique_id,
    city,
    state
from {{ ref('stg_customers') }}