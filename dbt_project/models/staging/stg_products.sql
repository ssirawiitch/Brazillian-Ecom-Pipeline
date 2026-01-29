select
    p.product_id,
    t.product_category_name_english as category_name
from {{ source('olist_raw', 'products') }} p
left join {{ source('olist_raw', 'category name') }} t 
    on p.product_category_name = t.product_category_name