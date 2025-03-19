import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')


# SQLite (`Data Pipeline`) ეტაპები
pipeline_steps = [
    ("1 მონაცემების გენერაცია", "python data/generate_data.py"),
    ("2 Bronze Layer - დაუმუშავებელი მონაცემების დამუშავება", "python sqlite_pipeline/bronze_layer.py"),
    ("3 Silver Layer - გაწმენდა და ნორმალიზაცია", "python sqlite_pipeline/silver_layer.py"),
    ("4 Gold Layer - ანგარიშგება და აგრეგაცია", "python sqlite_pipeline/gold_layer.py"),
]

def run_pipeline():
    print("\n **SQLite მონაცემთა მილსადენის (Data Pipeline) გაშვება დაიწყო...**\n")

    for step_name, command in pipeline_steps:
        print(f" მიმდინარეობს: {step_name}...")
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, encoding="utf-8")
            print(f" {step_name} დასრულდა წარმატებით!")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f" შეცდომა ეტაპზე: {step_name}!\n{e.stderr}")
            break

    print("\n **SQLite მონაცემთა მილსადენის გაშვება დასრულდა!**")

if __name__ == "__main__":
    run_pipeline()


