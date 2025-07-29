import yaml
import argparse
import os
from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage
import zipfile
import pandas as pd

def load_config():
    #load from cli
    parser = argparse.ArgumentParser()
    parser.add_argument("--download_dir", default=None)
    parser.add_argument("--download_dataset_name", default=None)
    parser.add_argument("--kaggle_dataset", default=None) 
    parser.add_argument("--gcs_bucket_name", default=None)
    parser.add_argument("--gcs_destination_folder", default=None)
    
    args = parser.parse_args()

    return vars(args)

#-------Kaggle download to local directory-------

def download_kaggle_dataset(dataset_name, download_dir):
    os.makedirs(download_dir, exist_ok=True)

    if os.path.exists(os.path.join(download_dir, f"{config['download_dataset_name']}.csv")):
        print(f"Dataset {dataset_name} already exists in {download_dir}, skipping download.")
        return
    
    api = KaggleApi()
    api.authenticate()
    print(f"Downloading {dataset_name} to {download_dir}...")
    api.dataset_download_files(dataset_name, path=download_dir, unzip=True)
    print("Download completed.")  

def convert_csv_to_parquet(download_dir, dataset_name):
    csv_file_path = os.path.join(download_dir, f"{dataset_name}.csv")
    parquet_file_path = os.path.join(download_dir, f"{dataset_name}.parquet")

    if not os.path.exists(csv_file_path):
        print(f"CSV file {csv_file_path} does not exist.")
        return

    df = pd.read_csv(csv_file_path)
    df.to_parquet(parquet_file_path, index=False)
    os.remove(csv_file_path)  
    print(f"Converted {csv_file_path} to {parquet_file_path}.")

#-------Upload to GCS bucket-------
def upload_to_gcs(bucket_name, source_dir, destination_folder):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for file_name in os.listdir(source_dir):
        source_file_path = os.path.join(source_dir, file_name)

        if os.path.isfile(source_file_path):
            blob_path = os.path.join(destination_folder, file_name)
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(source_file_path)
            print(f"Uploaded {file_name} to gs://{bucket_name}/{blob_path}")



if __name__ == "__main__":

    config = load_config()

    download_kaggle_dataset(config['kaggle_dataset'], config['download_dir'])
    convert_csv_to_parquet(config['download_dir'], config['download_dataset_name'])
    upload_to_gcs(config['gcs_bucket_name'], config['download_dir'], config['gcs_destination_folder'])



