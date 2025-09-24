{{ config(materialized='view') }}

with articlesdata as (
  select *,
    row_number() over(partition by id order by extracted_at desc) as rn
  from {{ source('staging','enriched_news_articles') }}
  where id is not null 
)
select
    cast (id as string) as article_id,
    {{ dbt_utils.generate_surrogate_key(['source']) }} as source_id,
    {{ dbt_utils.generate_surrogate_key(['author']) }} as author_id,
    cast (source as string) as source,
    cast (title as string) as article_title,
    cast (author as string) as author,
    cast(published_date as timestamp) as published_date,
    cast(extracted_at as timestamp) as extracted_at,
    cast (language as string) as language,
    {{dbt.safe_cast("polarity", api.Column.translate_type("float")) }} as polarity,
    {{dbt.safe_cast("subjectivity", api.Column.translate_type("float")) }} as subjectivity,
    cast(sentiment_category as string) as sentiment_category,
    persons,
    organizations,
    locations,
    {{ dbt.safe_cast("topic_id", api.Column.translate_type("int64")) }} as topic_id,
    safe_cast(topic_keywords as string) as topic_keywords,
    safe_cast(topic_label as string)    as topic_label
    
from articlesdata
where rn = 1

{% if var('is_test_run', default=true) %}
limit 100
{% endif %}
