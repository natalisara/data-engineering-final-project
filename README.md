# მონაცემთა Pipeline-ის პროექტი (Data Pipeline Project)

## პროექტის აღწერა

ეს პროექტი წარმოადგენს მონაცემთა დამუშავების Pipeline-ს, რომელიც იყენებს **SQLite3**-ს ადგილობრივ დამუშავებისთვის და **AWS S3**-ს ღრუბლოვან საცავად. Pipeline აგებულია **Medallion Architecture**-ის პრინციპით, რომელიც მოიცავს **Bronze**, **Silver** და **Gold** ფენებს. პროექტი ახდენს მონაცემთა გენერაციას, დამუშავებას, AWS S3-ზე ატვირთვას და ავტომატურ დამუშავებას **AWS Lambda**-ს გამოყენებით.

## ამოცანის აღწერა
ბიზნეს პროცესებში დარიცხვები და გადახდები მნიშვნელოვან როლს თამაშობს. ორგანიზაციებს სჭირდებათ კლიენტების ბალანსის მონიტორინგი, დებიტორების იდენტიფიცირება და საბუთის ტიპის მიხედვით ფინანსური ანალიზის ჩატარება.

ეს პროექტი ეყრდნობა დარიცხვების და გადახდების მონაცემებს, რომელიც მოიცავს:

- ტრანზაქციის თარიღს
- კლიენტის კოდს
- დარიცხული/გადახდილი თანხის რაოდენობას
- ოპერაციის საბუთის ტიპს (რომელ საბუთს უკავშირდება გადახდა/დარიცხვა)

მიზანია:
- კლიენტების ბალანსის გაანგარიშება დარიცხვებისა და გადახდების საფუძველზე
- ყველაზე დიდი ბრუნვის მქონე კლიენტების იდენტიფიცირება
- დებიტორების გამოვლენა (კლიენტები, რომლებსაც აქვთ დავალიანება)

## **პროექტის სტრუქტურა**

```plaintext
project-root/
├── data/                        # მონაცემთა დირექტორია
│   ├── transaction.xls          # საწყისი მონაცემები
│   ├── generate_data.py         # მონაცემთა გენერაციის სკრიპტი
│
├── sqlite_pipeline/             # SQLite ETL Pipeline
│   ├── create_tables.py         # ცხრილების შექმნა
│   ├── bronze_layer.py          # Bronze მონაცემთა დამუშავება
│   ├── silver_layer.py          # Silver მონაცემთა დამუშავება
│   ├── gold_layer.py            # Gold მონაცემთა აგრეგაცია
│   ├── main.py                  # მთავარი pipeline
│
├── aws/                         # AWS კომპონენტები
│   ├── lambda/
│   │   ├── bronze_to_silver.py  # Bronze → Silver გადასვლა
│   │   ├── silver_to_gold.py    # Silver → Gold გადასვლა
│   ├── create_lambda_zip.py     # Lambda ფაილების შეკუმშვა
│   ├── upload_to_s3.py          # მონაცემთა ატვირთვა S3-ზე
│
├── terraform/                    # Terraform კონფიგურაცია
│   ├── modules/
│   │   ├── s3/                   # S3 ბაკეტის მოდული
│   │   ├── lambda/               # Lambda მოდული
│   ├── main.tf                   # მთავარი კონფიგურაცია
│
├── terragrunt/                    # Terragrunt კონფიგურაცია
│   ├── terragrunt.hcl             # მთავარი კონფიგურაცია
│   └── env/
│       ├── dev/                   # Development გარემო
│       ├── prod/                  # Production გარემო
│
├── requirements.txt               # Python ბიბლიოთეკები
├── main.py                        # Pipeline-ის მთავარი სკრიპტი
├── README.md                      # პროექტის დოკუმენტაცია
└── .gitignore                     # Git-ის გამორიცხული ფაილები
```

## **Medallion Architecture (Bronze, Silver, Gold Layers)**

პროექტი იყენებს **Medallion Architecture**-ს მონაცემთა ორგანიზებისთვის, რაც უზრუნველყოფს მონაცემთა ხარისხისა და სანდოობის ზრდას თითოეულ ეტაპზე:

- **Bronze Layer** (Raw Data) – შეიცავს დაუმუშავებელ მონაცემებს, რომლებიც ატვირთულია **AWS S3 Bronze Bucket**-ში ან ინახება ადგილობრივ **SQLite** ბაზაში.
- **Silver Layer** (Cleansed Data) – ამ ფენაში მონაცემები იწმინდება, ნორმალიზდება და ხორციელდება ტრანსფორმაციები, რაც იწვევს მონაცემთა ხარისხის გაუმჯობესებას.
- **Gold Layer** (Aggregated Data) – საბოლოო ფენა, სადაც მონაცემები არის მთლიანად დამუშავებული, აგრეგირებული და მზად არის ანალიტიკისთვის.

## **ტექნიკური დეტალები**

### 1. **მონაცემთა გენერაცია**
Python-ის სკრიპტი `generate_data.py` ქმნის სინთეტიკურ მონაცემებს და ინახავს **transaction.xls**-ში, რომელიც შემდეგ Bronze ფენაში იტვირთება.

### 2. **SQLite Pipeline**
მონაცემთა დამუშავება ხდება **SQLite3**-ის გამოყენებით:
- `bronze_layer.py` – იღებს **transaction.xls**-დან მონაცემებს და ინახავს **Bronze** ფენაში.
- `silver_layer.py` – ასუფთავებს და ნორმალიზებას უკეთებს მონაცემებს.
- `gold_layer.py` – ახორციელებს აგრეგაციას და ანალიტიკურ დამუშავებას.

### 3. **AWS ინტეგრაცია**
მონაცემთა დამუშავების შემდეგ ისინი იტვირთება **AWS S3**-ის შესაბამის **Bronze, Silver და Gold ბაკეტებში** (`upload_to_s3.py`).

**Lambda ფუნქციები**:
- `bronze_to_silver.py` – ამუშავებს **Bronze** მონაცემებს და ინახავს **Silver** ბაკეტში.
- `silver_to_gold.py` – იღებს **Silver** მონაცემებს და ინახავს **Gold** ბაკეტში.

### 4. **Infrastructure as Code (IaC)**
პროექტი იყენებს **Terraform** და **Terragrunt** ინსტრუმენტებს AWS ინფრასტრუქტურის სამართავად:
- `terraform/modules/s3/` – S3 ბაკეტების შექმნა.
- `terraform/modules/lambda/` – Lambda ფუნქციების კონფიგურაცია.
- `terraform/main.tf` – საერთო ინფრასტრუქტურის კონფიგურაცია.
- `terragrunt/env/dev/` – Development გარემოს კონფიგურაცია.
- `terragrunt/env/prod/` – Production გარემოს კონფიგურაცია.

## **გაშვების ინსტრუქცია**

### **1. მოთხოვნები**
პროექტის გაშვებისთვის საჭიროა:
- **Python 3.x** და დამოკიდებულებები (`pip install -r requirements.txt`)
- **Terraform & Terragrunt**
- **AWS CLI** (კონფიგურირებული შესაბამისი უფლებებით)

### **2. პროექტის გაშვება**
```bash
# მონაცემთა გენერაცია
python data/generate_data.py

# Lambda ფუნქციების შეკუმშვა
python aws/create_lambda_zip.py

# Terraform-ის გაშვება
cd terraform && terraform apply -auto-approve

# Terragrunt-ის გაშვება
cd terragrunt/env/dev && terragrunt run-all apply --auto-approve

# მონაცემების ატვირთვა S3-ზე
python aws/upload_to_s3.py
```

## **საფინალო შენიშვნები**
- **პროექტი სრულად იყენებს Medallion Architecture-ს მონაცემთა ორგანიზებისთვის.**
- **Infrastructure as Code პრინციპით ინფრასტრუქტურა ავტომატიზირებულია Terraform & Terragrunt-ით.**
- **მონაცემთა ინტეგრაცია სრულდება AWS S3 & Lambda-ების გამოყენებით.**

📌 **პროექტის სრული კოდი, ინსტრუქციები და დოკუმენტაცია მოცემულია https://github.com/natalisara/data-engineering-final-project რეპოზიტორიაში.** 🚀




