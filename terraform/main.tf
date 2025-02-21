locals {
  secrets = {
    "TF_API_TOKEN" : var.TF_API_TOKEN,
    "NUGET_GITHUB_USER" : var.NUGET_GITHUB_USER,
    "NUGET_GITHUB_TOKEN" : var.NUGET_GITHUB_TOKEN,
  }
}

module "secrets" {
  for_each = local.secrets

  source  = "app.terraform.io/okkema/secret/github"
  version = "~> 0.2"

  repository = var.github_repository
  key        = each.key
  value      = each.value
}
