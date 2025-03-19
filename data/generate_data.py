import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_file = "data/Transactions.xlsx"

if not os.path.exists(excel_file):
    print(f" Excel ფაილი ვერ მოიძებნა: {excel_file}")
    exit()

# Excel ფაილის ჩატვირთვა (ყველა Sheet-ის წაკითხვა)
xls = pd.ExcelFile(excel_file)
sheets = xls.sheet_names

# ყველა Sheet-ის შენახვა Parquet ფორმატში
for sheet in sheets:
    df = xls.parse(sheet)  # თითოეული Sheet-ის DataFrame-ად გადაკეთება
    parquet_file = f"data/{sheet.lower()}.parquet"  # ფაილის სახელი
    df.to_parquet(parquet_file, engine="pyarrow", index=False)  # შენახვა Parquet-ში
    print(f"{sheet} Sheet შეინახა {parquet_file} ფაილში!")

print("ყველა მონაცემი წარმატებით გარდაიქმნა Parquet ფორმატში!")

