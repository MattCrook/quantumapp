variable "project_id" {
    description = "The project id of the current project as shown in GCP"
    type        = string
    default     = "quantum-coasters"
}

variable "region" {
    description = "The region of the current project"
    type        = string
    default     = "us-central1"
}

variable "db_remote_state_key" {
    description = "The prefix of the key in the Cloud Storage bucket used for the database's remote state storage"
    type        = string
    default     = "global/terraform.tfstate"
}

variable "enable_logging" {
    description = "If set to true, enables logging and creates a GCS bucket to store the logging files"
    type        = bool
    default     = false
}

variable "enable_bucket_object_acl" {
    description = "If set to true, enables object ACL bucket and creates a GCS bucket to store the ACL files, and [google_storage_default_object_acl] and [google_storage_object_acl] and [google_storage_bucket_object]"
    type        = bool
    default     = false
}

variable "iam_members" {
    description = "List of Service Accounts, Users, etc..to give IAM memebership to a new member tf_state bucket. Updates the IAM policy to grant a role to a new member."
    type        = list(string)
    default     = ["user:matt.crook11@gmail.com"]


variable acl { type = "list" default = [] }
variable object_name {}
variable filename {}
variable content {}
variable content_type { default = "" }
