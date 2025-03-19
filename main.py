import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

def run_pipeline():
    print("მიმდინარეობს Pipeline-ის გაშვება...\n")

    pipeline_steps = [
        ("1 მონაცემების გენერაცია", "python data/generate_data.py"),
        ("2 Lambda ფუნქციების შეკუმშვა (ZIP)", "python aws/create_lambda_zip.py"),
        ("3 AWS ინფრასტრუქტურის შექმნა (Terraform)", "cd terraform && terraform apply -auto-approve"),
        ("4 Terragrunt ინფრასტრუქტურის შექმნა (Terragrunt Apply)",
         'cd terragrunt/env/dev && "C:/Program Files/Terragrunt/terragrunt.exe" apply --auto-approve'),
        ("5 მონაცემების ატვირთვა AWS S3-ზე", "python aws/upload_to_s3.py"),
    ]

    for step_name, command in pipeline_steps:
        print(f"\n მიმდინარეობს: {step_name}...")
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, encoding="utf-8")
            print(f" {step_name} წარმატებით დასრულდა!")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f" შეცდომა ეტაპზე: {step_name}!\n{e.stderr}")
            break

    print("\n **Pipeline-ის გაშვება წარმატებით დასრულდა!** ")


if __name__ == "__main__":
    run_pipeline()
