provider "google" {
  project     = var.project_id
  region      = "us-central1"
}

terraform {
  required_version = ">= 0.13"
}

resource "google_sql_database_instance" "master" {
  project          = var.project_id
  name             = "quantumcoastersdb2"
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
  name      = "quantumcoastersdb2"
  charset   = "UTF8"
  collation = "en_US.UTF8"
  instance  = google_sql_database_instance.master.name
}

resource "google_sql_user" "users" {
  project         = var.project_id
  name            = "quantumcoastersdb2"
  instance        = google_sql_database_instance.master.name
  password        = "password"
  # password = random_string.password.result
  deletion_policy = "ABANDON"
}


resource "random_id" "secret" {
  byte_length = 4
}

resource "google_secret_manager_secret" "django_secret" {
  provider  = google-beta
  project   = var.project_id
  secret_id = "django-settings-${random_id.secret.hex}"

  labels = {
    label = "django-settings"
  }
}

resource "google_secret_manager_secret_version" "django_secret" {
  project     = var.project_id
  provider    = google-beta
  secret      = google_secret_manager_secret.my-secret.id
  secret_data = file("../../.env")
}

resource "google_secret_manager_secret_iam_member" "my-app" {
  provider  = google-beta
  secret_id = google_secret_manager_secret.django_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "user:mattcrook11@gmail.com"
}
