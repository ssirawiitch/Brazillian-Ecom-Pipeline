select
    product_id,
    category_name
from {{ ref('stg_products') }}