output "bucket_name" {
  description = "The name of the GCS bucket created"
  value       = google_storage_bucket.demo_bucket.name
}

output "dataset_id" {
  description = "The ID of the BigQuery dataset created"
  value       = google_bigquery_dataset.demo_dataset.dataset_id
}