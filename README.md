# 🇰🇪 Kenya News Articles Analytics Pipeline  

## Problem Statement
Kenya generates thousands of daily news articles capturing critical political, social, and economic events. However, this unstructured text makes it difficult to extract insights like key topics, sentiment trends, and named entities.  
## Solution
This project solves this problem by establishing an automated ELT pipeline that:  
- **Extracts** raw, news data.  
- **Enriches** with NLP features (sentiment, entities, language detection, topic modeling).  
- **Transforms** into a **Star Schema designed and materialized through dbt, inside BigQuery**.
- Visualizes insights in Metabase.

## Dataset
The project uses a [Kaggle dataset](https://www.kaggle.com/datasets/enockmokua/kenya-news-articles) of over 5,700 web-scraped Kenyan news articles published between 2018 and 2025.  
Each record contains the article’s title, publication date, author, source and content.

## Tools
- **Python scripts** – For data ingestion, processing, and NLP enrichment. 
- **Terraform** – For resource provisioning in GCP.  
- **Google Cloud Platform (GCP)** – Cloud infrastructure:  
  - **VM Instance** – To run the project.  
  - **Google Cloud Storage (GCS)** – For storing raw data files.
  - **BigQuery** – Cloud data warehouse for storing and querying structured datasets.
- **dbt (Data Build Tool)** – For transforming and modelling data into a Star Schema.
- **Kestra** – Orchestration tool for the ELT workflow.
- **Docker** – To run the Kestra and Metabase containers.
- **Metabase** – For creating a dashboard for visualisation.

## Architecture
![Kenya News Data Pipeline Architecture](https://github.com/maureen-githaiga/kenya-news-data-pipeline/blob/main/architecture(1).png)

## Dashboard
A simple dashboard built to visualize key insights from the Kenya news articles dataset. It demonstrates the pipeline’s analytical output but can be extended for more complex analysis.
![Dashboard](https://github.com/maureen-githaiga/kenya-news-data-pipeline/blob/main/kenya_news_analytics_dashboard.jpeg)

## To reproduce





  

