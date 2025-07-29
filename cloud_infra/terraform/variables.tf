variable "credentials" {
    description = "Credentials for accessing the cloud provider"
    type        = string
  
}

variable "projectid" {
    description = "The ID of the project where resources will be created"
    type        = string
}

variable "region" {
    description = "The region where the resources will be deployed"
    type        = string
}
variable "location" {
    description = "The location for the resources"
    type        = string
}

variable "bq_dataset_name" {
    description = "The name of the BigQuery dataset to be created"
    type        = string
  
}

variable "gcs_bucket_name" {
    description = "The name of the Google Cloud Storage bucket to be created"
    type        = string
  
}

variable "gcs_storage_class" {
    description = "The storage class for the Google Cloud Storage bucket"
    type        = string
  
}