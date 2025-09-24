{{config(
    materialized='table'
)}}
with articlesdata as (
    select *
    from {{ ref('stg_news_articles_data') }}
),
dim_authors as (
    select *
    from {{ ref('dim_authors') }}
),
dim_sources as (
    select *
    from {{ ref('dim_sources') }}
),
dim_topics as (
    select *
    from {{ ref('dim_topics') }}
)
select 
 articlesdata.article_id,
 articlesdata.published_date,
 articlesdata.extracted_at,

 --author
 articlesdata.author_id,
 COALESCE(REGEXP_EXTRACT(articlesdata.author, r'by (.*?) on'), 'Unknown') as author_name,

 --source
 articlesdata.source_id,
 coalesce(articlesdata.source, 'Unknown') as source_name,

 --topic
 articlesdata.topic_id,
 articlesdata.topic_label,
 articlesdata.topic_keywords,

 articlesdata.polarity,
 articlesdata.subjectivity,
 articlesdata.sentiment_category,

 articlesdata.persons,
 articlesdata.organizations,
 articlesdata.locations

from articlesdata articlesdata
left join dim_authors authors on articlesdata.author_id = authors.author_id
left join dim_sources sources on articlesdata.source_id = sources.source_id
left join dim_topics topics on articlesdata.topic_id = topics.topic_id 