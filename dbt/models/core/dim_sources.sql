{{config(
    materialized = 'table'
)}}
select 
    source_id,
    source as source_name
from {{ref('stg_news_articles_data')}}
group by 1,2