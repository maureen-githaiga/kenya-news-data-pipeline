from google.cloud import bigquery
import os
import argparse

def load_config():
    #load from cli
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", default=None)
    parser.add_argument("--gcs_uri", default=None)
    parser.add_argument("--bq_dataset_name", default=None)
    
    args = parser.parse_args()

    return vars(args)

#-------load from gcs bucket to bigquery-------
def load_to_bigquery(gcs_uri, dataset_id, project_id):

    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_id)
    table_name = os.path.basename(gcs_uri.split('.')[0]) 
    table_id = f"{project_id}.{dataset_id}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    print(f"Loading data from {gcs_uri} into BigQuery table {table_id}...")
    load_job = client.load_table_from_uri(
        gcs_uri,
        table_id,
        job_config=job_config
    )
    load_job.result()  

    print(f"Loaded {load_job.output_rows} rows into {table_id}.")

if __name__ == "__main__":
    config = load_config()
    load_to_bigquery(config['gcs_uri'], config['bq_dataset_name'], config['project_id'])
