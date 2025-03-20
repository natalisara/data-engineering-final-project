import boto3
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

# AWS გასაღებების წამოღება
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
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
