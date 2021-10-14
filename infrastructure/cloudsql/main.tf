provider "google" {
  project     = var.project_id
  region      = "us-central1"
}

terraform {
  required_version = ">= 0.13"
}

resource "google_sql_database_instance" "master" {
  project          = var.project_id
  name             = "quantumcoastersdb"
  database_version = "POSTGRES_13"
  region           = "us-central1"
  deletion_protection = false

  settings {
    tier = "db-custom-2-13312"
    disk_autoresize = true
    disk_size       = 10
    disk_type       = "PD_SSD"
    pricing_plan    = "PER_USE"

    ip_configuration {
        ipv4_enabled        = true
        require_ssl         = false
    }
  }
}

// resource "random_string" "password" {
//   length = 16
//   special = true
// }

resource "google_sql_database" "master" {
  project   = var.project_id
  name      = "quantumcoastersdb"
  charset   = "UTF8"
  collation = "en_US.UTF8"
  instance  = google_sql_database_instance.master.name
}

resource "google_sql_user" "users" {
  project         = var.project_id
  name            = "quantumcoastersdb"
  instance        = google_sql_database_instance.master.name
  password        = "password"
  # password = random_string.password.result
  deletion_policy = "ABANDON"
}
