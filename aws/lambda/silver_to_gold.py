import boto3
import pandas as pd
import io
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# S3 კლიენტი
s3 = boto3.client("s3")

# S3 Bucket-ები
SILVER_BUCKET = "my-data-pipeline-silver"
GOLD_BUCKET = "my-data-pipeline-gold"

def lambda_handler(event, context):
    try:
        # მიღებული ფაილის ინფორმაცია
        print(f" მიღებული `event`: {json.dumps(event)}")

        file_key = event["Records"][0]["s3"]["object"]["key"]
        print(f" ახალი ფაილი მიღებულია: {file_key}")

        if "silver" not in file_key:
            print(" შეცდომა: ფაილის სახელი არ შეესაბამება silver bucket-ის მონაცემებს.")
            return {"statusCode": 400, "body": "ფაილის დასახელება არასწორია!"}

        # ფაილის წამოღება S3-დან
        response = s3.get_object(Bucket=SILVER_BUCKET, Key=file_key)
        df_silver = pd.read_parquet(io.BytesIO(response["Body"].read()))

        print(f" მონაცემები წარმატებით ჩაიტვირთა Silver Bucket-დან ({file_key})")

        # მონაცემთა აგრეგაცია (მაგალითად, კლიენტების ბალანსების დათვლა)
        df_gold = df_silver.groupby("customerpayer", as_index=False).agg({"amount_balance": "sum"})

        print(f" მონაცემები წარმატებით დაითვალა და აგრეგაცია შესრულდა!")

        # დამუშავებული ფაილის ატვირთვა Gold Bucket-ში
        buffer = io.BytesIO()
        df_gold.to_parquet(buffer, index=False)
        buffer.seek(0)

        new_file_key = file_key.replace("silver", "gold")
        s3.put_object(Bucket=GOLD_BUCKET, Key=new_file_key, Body=buffer.getvalue())

        print(f" მონაცემები გადატანილია S3-ის Gold Bucket-ში → {new_file_key}")

        return {"statusCode": 200, "body": f"ფაილი წარმატებით დამუშავდა და Gold Bucket-ში გადატანილი: {new_file_key}"}

    except Exception as e:
        print(f" შეცდომა: {str(e)}")
        return {"statusCode": 500, "body": f"შეცდომა დამუშავებისას: {str(e)}"}
