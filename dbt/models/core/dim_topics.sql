{{config(
    materialized = 'table'
)}}
select 
    topic_id,
    topic_label,
    topic_keywords
from {{ref('stg_news_articles_data')}}
group by 1,2,3