terraform {
    source = "source = ../../../terraform"
//     source = "${get_repo_root()}/terraform"
//   source = "../../../terraform"
}

inputs = {
  environment = "prod"
  bucket_name = "my-data-pipeline-prod"
}


