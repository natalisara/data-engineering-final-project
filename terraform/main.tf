terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state-natali"
    key            = "global/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
    use_lockfile   = true
#     dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = "eu-north-1"
}

# S3 მოდულის გამოძახება
module "s3" {
  source = "./modules/s3"
}

# Lambda მოდულის გამოძახება
module "lambda" {
  source = "./modules/lambda"

  bronze_bucket_name = module.s3.bronze_bucket_name
  silver_bucket_name = module.s3.silver_bucket_name
  gold_bucket_name   = module.s3.gold_bucket_name
}
