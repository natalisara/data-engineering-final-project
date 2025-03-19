import boto3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# AWS კონფიგურაცია (მოითხოვს AWS Access Key-ს!)
AWS_ACCESS_KEY = "AKIAWCYYAG34FY4TYQRW"
AWS_SECRET_KEY = "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"
AWS_REGION = "eu-north-1"

# S3 Bucket-ების სახელები
BUCKETS = {
    "bronze": "my-data-pipeline-bronze",
    "silver": "my-data-pipeline-silver",
    "gold": "my-data-pipeline-gold"
}

# შექმნა S3 კლიენტი
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# მონაცემთა ატვირთვა S3-ზე
def upload_to_s3(file_path, bucket, s3_key):
    try:
        s3.upload_file(file_path, bucket, s3_key)
        print(f" ატვირთულია {file_path} → s3://{bucket}/{s3_key}")
    except Exception as e:
        print(f" შეცდომა: {e}")

# ატვირთვა Bronze Bucket-ში
upload_to_s3("data/transactions.parquet", BUCKETS["bronze"], "bronze/transactions.parquet")

# ატვირთვა Silver Bucket-ში
upload_to_s3("data/silver_transactions.parquet", BUCKETS["silver"], "silver/silver_transactions.parquet")

# ტვირთვა Gold Bucket-ში
upload_to_s3("data/gold_aggregations.parquet", BUCKETS["gold"], "gold/gold_aggregations.parquet")
