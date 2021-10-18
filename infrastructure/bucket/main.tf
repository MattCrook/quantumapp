provider "google" {
    # To login run: gcloud beta auth application-default login
    project     = var.project_id
    region      = var.region
}

// terraform {
//     backend "remote" {
//         bucket      = "quantum-core-tf-state"
//         prefix      = "global/terraform.tfstate"
//     }
// }

#########################
# GCS bucket to store logging, as referenced in the state bucket.
##########################
resource "google_storage_bucket" "logging_bucket" {
    count = var.enable_logging ? 1 : 0

    name          = "tf-quantumapp-logging-bucket"
    location      = "US"
    storage_class = "STANDARD"
    project       = "${var.project_id}"
    # This is only here so we can destroy the bucket as part of automated tests. You should not copy this for production usage.
    force_destroy = true

    versioning {
        enabled = false
    }

    labels {
        env = "prod"
        bucket = "logging"
    }

    lifecycle_rules = [{
        action = {
        type = "Delete"
        }
        condition = {
        age        = 365
        with_state = "ANY"
        }
    }]

    iam_members = [{
        role   = "roles/storage.admin"
        member = "user:matt.crook11@gmail.com"
    }]
}

###########################
# GCS bucket that Authoritatively manages the default object ACLs for a Google Cloud Storage bucket without managing the bucket itself
###########################
resource "google_storage_bucket" "object_acl_bucket" {
    count = var.enable_bucket_object_acl ? 1 : 0

    project       = "${var.project_id}"
    name          = "tf-quantum-acl-bucket"
    location      = "US"
    storage_class = "STANDARD"
    # This is only here so we can destroy the bucket as part of automated tests. You should not copy this for production usage.
    force_destroy = true

    versioning {
        enabled = false
    }

    labels {
        env = "prod"
        bucket = "ACL"
    }

    lifecycle_rules = [{
        action = {
        type = "Delete"
        }
        condition = {
        age        = 365
        with_state = "ANY"
        }
    }]

    iam_members = [{
        role   = "roles/storage.admin"
        member = "user:matt.crook11@gmail.com"
    }]
}

#################################
# Our gcs bucket to store the state. Will use "gcs" as backend which is this bucket.
# Google Cloud Platform like most of the remote backends natively supports locking.
# This bucket for tf state
##################################
resource "google_storage_bucket" "tf_state" {
    project       = "${var.project_id}"
    name          = "tf-quantum-core-tf-state"
    location      = "US"
    storage_class = "STANDARD"
    # This is only here so we can destroy the bucket as part of automated tests. You should not copy this for production usage.
    force_destroy = true

    versioning {
        enabled = true
    }

    labels {
        env = "stage"
        bucket = "state"
    }

    logging {
        log_bucket = var.enable_logging ? google_storage_bucket.logging_bucket.name : null
    }

    lifecycle_rules = [{
        action = {
        type = "Delete"
        }
        condition = {
        age        = 365
        with_state = "ANY"
        }
    }]

    iam_members = [{
        role   = "roles/storage.admin"
        member = "user:matt.crook11@gmail.com"
    }]
}

#################################
# GCS bucket for storing static files from Qauntum app build for App Engine
##################################
resource "google_storage_bucket" "quantumapp_gae_storage" {
    project       = "${var.project_id}"
    name          = "quantumapp.appspot.com"
    location      = "US"
    storage_class = "STANDARD"
    # This is only here so we can destroy the bucket as part of automated tests. You should not copy this for production usage.
    force_destroy = true

    versioning {
        enabled = true
    }

    labels {
        env = "prod"
        bucket = "gae-storage"
    }

    logging {
        log_bucket = var.enable_logging ? google_storage_bucket.logging_bucket.name : null
    }

    lifecycle_rules = [{
        action = {
        type = "Delete"
        }
        condition = {
        age        = 365
        with_state = "ANY"
        }
    }]

    iam_members = [{
        role   = "roles/storage.admin"
        member = "user:matt.crook11@gmail.com"
    }]
}

resource "google_storage_bucket_iam_member" "members" {
    for_each = {
        for _, m in var.iam_members : "${m.role} ${m.member} => m
    }
    bucket = "${google_storage_bucket.tf_state.name}"
    role   = "${each.value.role}"
    member = "${each.value.member}"
}


##################
# Object ACL's for ACL bucket and Logging bucket
# Only apply if either is enabaled
###############
resource "google_storage_bucket_acl" "tf-bucket-acl" {
    bucket      = "${google_storage_bucket.tf_state.name}"
    role_entity = ["${var.acl}"]
    depends_on  = ["google_storage_bucket.tf_state"]
}

resource "google_storage_bucket_acl" "logging-bucket-acl" {
    count = var.enable_logging ? 1 : 0

    bucket      = "${google_storage_bucket.logging_bucket.name}"
    role_entity = ["${var.acl}"]
    depends_on  = ["google_storage_bucket.logging_bucket"]
}

resource "google_storage_default_object_acl" "default-acl" {
    count = var.enable_bucket_object_acl ? 1 : 0

    bucket      = "${google_storage_bucket.object_acl_bucket.name}"
    role_entity = ["${var.acl}"]
}

resource "google_storage_object_acl" "object-acl" {
    count = var.enable_bucket_object_acl ? 1 : 0

    bucket      = "${google_storage_bucket.object_acl_bucket.name}"
    object      = "${var.object_name}"
    role_entity = ["${var.acl}"]
}

# Bucket Content
# Depends on if ACL bucket is created or not.
resource "google_storage_bucket_object" "object" {
    count = var.enable_bucket_object_acl ? 1 : 0

    name         = "${var.filename}"
    content      = "${var.content}"
    bucket       = "${var.object_bucket_name}"
    content_type = "${var.content_type}"
}
