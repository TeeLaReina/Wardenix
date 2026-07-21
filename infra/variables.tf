variable "do_token" {
  description = "DigitalOcean API token for the Wardenix project."
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Short name used to tag and identify Wardenix resources."
  type        = string
  default     = "wardenix"
}

variable "region" {
  description = "DigitalOcean region slug."
  type        = string
  default     = "fra1"
}

variable "ssh_public_key" {
  description = "SSH public key content, injected into the droplet."
  type        = string
  sensitive   = true
}
