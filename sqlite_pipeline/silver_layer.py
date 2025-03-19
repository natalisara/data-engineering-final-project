import sqlite3
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

# მონაცემთა ბაზის გახსნა
db_path = "data/transactions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Silver Layer ცხრილის შექმნა (გაწმენდილ მონაცემებზე)
cursor.execute("""
CREATE TABLE IF NOT EXISTS silver_transactions AS
SELECT DISTINCT 
    t.transactionid,
    t.documentid,
    t.servicetype,
    s.descrip AS service_description,
    t.doctype,
    d.description AS document_description,
    t.customerpayer,
    c.customername AS customer_name,
    amount,
    t.tax,
    (t.amount+t.tax)* bmodule as amount_balance,
    DATE(t.docdate) AS docdate,  
    DATE(t.insertdate) AS insertdate
FROM bronze_transactions t
LEFT JOIN service_type s ON t.servicetype = s.servicetype
LEFT JOIN doc_type d ON t.doctype = d.doctype
LEFT JOIN customer c ON t.customerpayer = c.customerpayer
WHERE t.amount IS NOT NULL  
AND t.docdate IS NOT NULL 
AND t.customerpayer IS NOT NULL; 
""")

conn.commit()
print(" Silver Layer მონაცემები წარმატებით შეიქმნა და გაიწმინდა!")

df_silver = pd.read_sql_query("SELECT * FROM silver_transactions;", conn)
df_silver.to_parquet("data/silver_transactions.parquet", index=False)
print(" Silver Layer მონაცემები შეინახა data/silver_transactions.parquet ფაილში!")

conn.close()
