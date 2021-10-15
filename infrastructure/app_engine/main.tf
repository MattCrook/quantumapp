provider "google" {
  project     = var.project_id
  region      = "us-central1"
}

terraform {
  required_version = ">= 0.13"
}

data "google_project" "project" {
  name       = "Quantum Coasters"
  project_id = "quantum-coasters"
}


resource "google_app_engine_application" "quantumapp" {
  project       = google_project.project.project_id
  location_id   = "us-central"
  auth_domain   = "gmail.com"
  database_type =  "CLOUD_DATASTORE_COMPATIBILITY"
}
