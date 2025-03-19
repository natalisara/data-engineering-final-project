# ✅ უკვე არსებული S3 ბაკეტების მონაცემების წამოღება
data "aws_s3_bucket" "bronze" {
  bucket = "my-data-pipeline-bronze"
}

data "aws_s3_bucket" "silver" {
  bucket = "my-data-pipeline-silver"
}

data "aws_s3_bucket" "gold" {
  bucket = "my-data-pipeline-gold"
}

# ✅ ბაკეტების სახელების output-ები
output "bronze_bucket_name" {
  value = data.aws_s3_bucket.bronze.id
}

output "silver_bucket_name" {
  value = data.aws_s3_bucket.silver.id
}

output "gold_bucket_name" {
  value = data.aws_s3_bucket.gold.id
}


# data "aws_s3_bucket" "bronze_existing" {
#   bucket = "my-data-pipeline-bronze"
# }
#
# resource "aws_s3_bucket" "bronze" {
#   bucket = "my-data-pipeline-bronze"
#
#   count = length(data.aws_s3_bucket.bronze_existing.id) > 0 ? 0 : 1  # თუ უკვე არსებობს, არ შექმნის
#
#   lifecycle {
#     prevent_destroy = true
#     ignore_changes  = [tags]
#   }
# }
#
# data "aws_s3_bucket" "silver_existing" {
#   bucket = "my-data-pipeline-silver"
# }
#
# resource "aws_s3_bucket" "silver" {
#   bucket = "my-data-pipeline-silver"
#
#   count = length(data.aws_s3_bucket.silver_existing.id) > 0 ? 0 : 1
#
#   lifecycle {
#     prevent_destroy = true
#     ignore_changes  = [tags]
#   }
# }
#
# data "aws_s3_bucket" "gold_existing" {
#   bucket = "my-data-pipeline-gold"
# }
#
# resource "aws_s3_bucket" "gold" {
#   bucket = "my-data-pipeline-gold"
#
#   count = length(data.aws_s3_bucket.gold_existing.id) > 0 ? 0 : 1
#
#   lifecycle {
#     prevent_destroy = true
#     ignore_changes  = [tags]
#   }
# }
#
# output "bronze_bucket_name" {
#   value = "my-data-pipeline-bronze"
# }
#
# output "silver_bucket_name" {
#   value = "my-data-pipeline-silver"
# }
#
# output "gold_bucket_name" {
#   value = "my-data-pipeline-gold"
# }
#
