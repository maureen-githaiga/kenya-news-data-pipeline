{{config(
    materialized = 'table'
)}}
select 
    distinct
    author_id,
    COALESCE(REGEXP_EXTRACT(author, r'by (.*?) on'), 'Unknown') as author_name
from {{ref('stg_news_articles_data')}}
