import sqlite3
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

db_path = "data/transactions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS gold_aggregations AS
SELECT 
    t.customerpayer,
    c.customername,
    SUM(t.amount_balance) AS total_balance,  
    COUNT(t.transactionid) AS total_transactions,  
    (SELECT doctype FROM silver_transactions GROUP BY doctype ORDER BY COUNT(*) DESC LIMIT 1) AS top_document,  
    (SELECT AVG(amount) FROM silver_transactions WHERE doctype in (5,6)) AS average_payment  
FROM silver_transactions t
LEFT JOIN customer c ON t.customerpayer = c.customerpayer
GROUP BY t.customerpayer, c.customername
ORDER BY total_balance DESC;
""")

# ტოპ 10 დებიტორი
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_debtors AS
SELECT customerpayer, customername, total_balance
FROM gold_aggregations
WHERE total_balance < 0
ORDER BY total_balance ASC
LIMIT 10;
""")

# ტოპ 10 კრედიტორი
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_creditors AS
SELECT customerpayer, customername, total_balance
FROM gold_aggregations
WHERE total_balance > 0
ORDER BY total_balance DESC
LIMIT 10;
""")

# საბუთების ტიპის მიხედვით თანხების გაერთიანება
cursor.execute("""
CREATE TABLE IF NOT EXISTS document_type_totals AS
SELECT t.doctype, d.description, SUM(t.amount) AS total_amount
FROM silver_transactions t
LEFT JOIN doc_type d ON t.doctype = d.doctype
GROUP BY t.doctype, d.description
ORDER BY total_amount DESC;
""")

# მომსახურების ტიპის მიხედვით თანხების დაჯამება
cursor.execute("""
CREATE TABLE IF NOT EXISTS service_type_totals AS
SELECT t.servicetype, s.descrip AS service_name,bmodule, SUM(t.amount) AS total_amount
FROM silver_transactions t
LEFT JOIN service_type s ON t.servicetype = s.servicetype
GROUP BY t.servicetype, s.descrip,s.bmodule
ORDER BY total_amount DESC;
""")

conn.commit()
print(" Gold Layer მონაცემები წარმატებით შეიქმნა!")

# მონაცემების შემოწმება
df_debtors = pd.read_sql_query("SELECT * FROM top_debtors;", conn)
df_creditors = pd.read_sql_query("SELECT * FROM top_creditors;", conn)
df_docs = pd.read_sql_query("SELECT * FROM document_type_totals;", conn)
df_services = pd.read_sql_query("SELECT * FROM service_type_totals;", conn)

df_creditors["total_balance"] = df_creditors["total_balance"].apply(lambda x: f"{x:,.2f}")
df_debtors["total_balance"] = df_debtors["total_balance"].apply(lambda x: f"{x:,.2f}")
df_services["total_amount"] = df_services["total_amount"].apply(lambda x: f"{x:,.2f}")
df_docs["total_amount"] = df_docs["total_amount"].apply(lambda x: f"{x:,.2f}")

print("\n ტოპ 10 დებეტორი:")
print(df_debtors)

print("\n ტოპ 10 კრედიტორი:")
print(df_creditors)

print("\n საბუთის ტიპების მიხედვით თანხები:")
print(df_docs)

print("\n მომსახურების ტიპების მიხედვით თანხები:")
print(df_services)

df_gold = pd.read_sql_query("SELECT * FROM gold_aggregations;", conn)
df_gold.to_parquet("data/gold_aggregations.parquet", index=False)
print(" Gold Layer მონაცემები შეინახა data/gold_aggregations.parquet ფაილში!")

conn.close()
