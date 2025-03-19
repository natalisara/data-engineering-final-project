import sqlite3
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# მონაცემთა ბაზის შექმნა
db_path = "data/transactions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Bronze Layer
cursor.execute("""
CREATE TABLE IF NOT EXISTS bronze_transactions (
    transactionid INTEGER PRIMARY KEY AUTOINCREMENT, 
    documentid INTEGER,
    servicetype INTEGER,
    doctype INTEGER,
    customerpayer INTEGER,
    amount REAL, 
    tax REAL, 
    docdate DATETIME,
    insertdate DATETIME
);
""")

# DocType
cursor.execute("""
CREATE TABLE IF NOT EXISTS doc_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctype INTEGER,  
    description TEXT
);
""")

# ServiceType
cursor.execute("""
CREATE TABLE IF NOT EXISTS service_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    servicetype INTEGER,
    descrip TEXT,
    bmodule INTEGER 
);
""")

#  Customer
cursor.execute("""
CREATE TABLE IF NOT EXISTS customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customerpayer INTEGER,
    customername TEXT
);
""")

conn.commit()  # ცვლილებების შენახვა

# მონაცემების ჩატვირთვა Parquet-დან

# Transactions (Bronze Layer)
df_transactions = pd.read_parquet("data/transactions.parquet")
df_transactions.to_sql("bronze_transactions", conn, if_exists="replace", index=False)

# DocType ცნობარის ჩატვირთვა
df_doc_type = pd.read_parquet("data/doctype.parquet")
df_doc_type = df_doc_type.rename(columns={"id": "id", "doctype": "doctype", "description": "description"})
df_doc_type.to_sql("doc_type", conn, if_exists="replace", index=False)

# ServiceType ცნობარის ჩატვირთვა
df_service_type = pd.read_parquet("data/servicetype.parquet")
df_service_type = df_service_type.rename(columns={"id": "id", "servicetype": "servicetype", "descrip": "descrip", "bmodule": "bmodule"})
df_service_type.to_sql("service_type", conn, if_exists="replace", index=False)

# Customer ცნობარის ჩატვირთვა
df_customer = pd.read_parquet("data/customer.parquet")
df_customer = df_customer.rename(columns={"id": "id", "customerpayer": "customerpayer", "customername": "customername"})
df_customer.to_sql("customer", conn, if_exists="replace", index=False)

print("ყველა მონაცემი ჩაიტვირთა Bronze Layer-ში სწორად!")

conn.close()
