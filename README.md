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
- **Python** – Used for data ingestion, processing, and NLP enrichment. 
- **Terraform** – Defines and provisions all GCP and cloud infrastructure resources.  
- **Google Cloud Platform (GCP)** – Provides cloud services: BigQuery (Data Warehouse), Cloud Storage (GCS) (Data Lake), and IAM.  
- **dbt (Data Build Tool)** – For transforming and modelling data into a Star Schema.
- **Kestra** – Workflow orchestration.
- **Docker** –  Containerization platform for orchestrator (Kestra) and visualisation (Metabase).
- **Metabase** – Dashboard.

## Architecture
![Kenya News Data Pipeline Architecture](https://github.com/maureen-githaiga/kenya-news-data-pipeline/blob/main/architecture(1).png)

## Star Schema Design  
The warehouse follows a **Star Schema** design for optimized analytics:  
- **Fact Table**:  
  - `fct_articles`: contains metrics like article_id, published_date, sentiment, polarity, subjectivity, topic_id, author_id, source_id.  
- **Dimension Tables**:  
  - `dim_authors`: maps author_id → author_name.  
  - `dim_sources`: maps source_id → source_name.  
  - `dim_topics`: maps topic_id → topic_label and keywords.  
This design allows efficient joins and flexible BI queries.

## Dashboard
A simple dashboard built to visualize key insights from the Kenya news articles dataset. It demonstrates the pipeline’s analytical output but can be extended for more complex analysis.
![Dashboard](https://github.com/maureen-githaiga/kenya-news-data-pipeline/blob/main/kenya_news_analytics_dashboard.jpeg)

### Insights
- **Sentiment Distribution**: The Majority of articles fall under positive, with the smallest proportion being negative.  
- **Topic Trends**: Most articles cover Education & Development and Agriculture. 
- **Top Named Entities**: Key figures such as *William Ruto* and *Uhuru Kenyatta* appear most frequently (who are the current and former president of Kenya, respectively).  
- **Organisations & Locations**: Mentions of government entities and major cities in Kenya and neighbouring countries.

## Challenges

- **Limited dataset size**: The dataset used contains a finite number of articles, which restricts the depth and variety of insights that can be derived. Larger datasets would strengthen the analytics.  
- **Single source**: The dataset originates from only one source. Incorporating multiple sources would provide richer perspectives, enhance topic diversity, and improve analytical accuracy.  
- **NLP scope**: The NLP processing implemented here was basic. A more thorough NLP pipeline, incorporating advanced entity resolution, sentiment analysis, and topic modelling, would yield deeper insights.  

## Reproducing the Project
To reproduce this project:  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/maureen-githaiga/kenya-news-data-pipeline.git
   cd kenya-news-data-pipeline 
   
2. Provision infrastructure with Terraform

   ```bash
    terraform init
    terraform apply
3. Set up permissions and secrets
   - Add your Kaggle API credentials (for dataset extraction).
   - Add your GCP service account credentials (for BigQuery & Cloud Storage).
   - Store these securely (as secret variables in Kestra (you can use a .env_encoded file; instructions ![here](https://kestra.io/docs/how-to-guides/secrets)).
4. Launch Kestra with the Docker Compose file in the orchestration directory.
   ```bash
   docker-compose up -d
  Open Kestra at http://localhost:8080. Import the flows from this repo, and run the pipeline.  
5. Run Metabase with Docker, connect to BigQuery as your datasource.
  
    ```bash
      docker run -d -p 3000:3000 --name metabase metabase/metabase

## Conclusion

This project demonstrates the creation of a complete end-to-end data pipeline, from raw data extraction to delivering structured analytics-ready datasets.  It shows how tools such as Terraform, dbt, Kestra, BigQuery, and Metabase can be used to automate workflows, transform unstructured data, and deliver actionable insights.  
Beyond the specific analytics achieved, the key outcome of this work is the practical learning gained in designing, orchestrating, and maintaining a data pipeline in a cloud environment.  

  

