import boto3
import pandas as pd
import io
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
# S3 კლიენტი
s3 = boto3.client("s3")

# S3 Bucket-ები (გარე ცვლადებად)
BRONZE_BUCKET = "my-data-pipeline-bronze"
SILVER_BUCKET = "my-data-pipeline-silver"

def lambda_handler(event, context):
    try:
        # მიღებული ფაილის ინფორმაცია
        print(f"მიღებული `event`: {json.dumps(event)}")

        file_key = event["Records"][0]["s3"]["object"]["key"]
        print(f"ახალი ფაილი მიღებულია: {file_key}")

        if "bronze" not in file_key:
            return {"statusCode": 400, "body": "ფაილის დასახელება არასწორია!"}

        # ფაილის წამოღება S3-დან
        response = s3.get_object(Bucket=BRONZE_BUCKET, Key=file_key)
        df_bronze = pd.read_parquet(io.BytesIO(response["Body"].read()))

        # მონაცემთა გაწმენდა (მაგალითად, null ველების წაშლა)
        df_silver = df_bronze.dropna()

        # დამუშავებული ფაილის ატვირთვა Silver Bucket-ში
        buffer = io.BytesIO()
        df_silver.to_parquet(buffer, index=False)
        buffer.seek(0)

        # შექმნილი ფაილის სახელის ფორმირება
        new_file_key = file_key.replace("bronze", "silver")
        s3.put_object(Bucket=SILVER_BUCKET, Key=new_file_key, Body=buffer.getvalue())

        print(f" დამუშავებული მონაცემები გადატანილია Silver Bucket-ში: {new_file_key}")

        return {"statusCode": 200, "body": f"ფაილი წარმატებით დამუშავდა: {new_file_key}"}

    except Exception as e:
        print(f" შეცდომა: {str(e)}")
        return {"statusCode": 500, "body": f"შეცდომა დამუშავებისას: {str(e)}"}
