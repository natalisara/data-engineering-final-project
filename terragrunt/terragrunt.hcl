terraform {
    source = "../terraform"
//     "${get_repo_root()}/terraform"
//   source = "../terraform"
}



remote_state {
  backend = "s3"
  config = {
    bucket         = "my-terraform-state-natali"
    key            = "global/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "eu-north-1"
}
EOF
}
