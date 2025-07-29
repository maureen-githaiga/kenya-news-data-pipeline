terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
    credentials = file(var.credentials)
    project     = var.projectid
    region      = var.region
}

resource "google_storage_bucket" "demo_bucket" {
    name          = var.gcs_bucket_name
    location      = var.location
    storage_class = var.gcs_storage_class

    lifecycle_rule {
        condition {
          
            age = 30

        }
        action {
            type = "Delete"

        }

    }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}