import os
import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')

LAMBDA_FUNCTIONS = ["bronze_to_silver", "silver_to_gold"]

LAMBDA_DIR = "aws/lambda"
os.makedirs(LAMBDA_DIR, exist_ok=True)  # ქმნის aws/lambda თუ არ არსებობს


def create_lambda_zip(lambda_name):
    """Lambda ფუნქციის კოდის შეკუმშვა ZIP-ში"""
    lambda_file = f"{LAMBDA_DIR}/{lambda_name}.py"
    zip_file = f"{LAMBDA_DIR}/{lambda_name}.zip"

    if not os.path.exists(lambda_file):
        print(f" ფაილი ვერ მოიძებნა: {lambda_file}")
        return

    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(lambda_file, os.path.basename(lambda_file))

    print(f" {lambda_name}.zip შექმნილია {zip_file}-ში")


# ყველა Lambda-სთვის ZIP ფაილის შექმნა
for func in LAMBDA_FUNCTIONS:
    create_lambda_zip(func)
