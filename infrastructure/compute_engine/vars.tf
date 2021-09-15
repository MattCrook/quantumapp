variable "project" {
  description = "Project ID as shown in GCP"
  type        = string
  default     = "quantum-coasters"
}

variable "members" {
  description = "Service account list of members"
  type        = list(string)
  default     = ["user:matt.crook@gmail.com"]
}

variable "region" {
  type        = string
  default     = "us-central1"
}

variable "zone" {
  type        = string
  default     = "us-central1-c"
}

variable "server_port" {
  description = "The port the server will use for HTTP requests"
  type        = number
  default     = 8000
}
