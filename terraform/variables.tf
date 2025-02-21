variable "github_repository" {}

# GitHub Actions Secrets
variable "TF_API_TOKEN" {
  sensitive = true
}
variable "NUGET_GITHUB_USER" {
  sensitive = true
}
variable "NUGET_GITHUB_TOKEN" {
  sensitive = true
}