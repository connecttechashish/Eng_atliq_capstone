# Databricks notebook source
# MAGIC %md
# MAGIC **This notebook is to generate silver layer data**

# COMMAND ----------

#Define ADLS Paths
bronze_base = "abfss://bronze@atliqdatalake.dfs.core.windows.net"
silver_base = "abfss://silver@atliqdatalake.dfs.core.windows.net"

# COMMAND ----------

#Read Bronze Data (All Tables)
orders_df = None
order_items_df = None
payments_df = None
customers_df = None
products_df = None
orders_df = spark.read.parquet(f"{bronze_base}/orders/")
order_items_df = spark.read.parquet(f"{bronze_base}/order_items/")
payments_df = spark.read.parquet(f"{bronze_base}/payments/")
customers_df = spark.read.parquet(f"{bronze_base}/customers/")
products_df = spark.read.parquet(f"{bronze_base}/products/")


# COMMAND ----------

# Silver Transformations (Spark Connect Safe) - Orders
from pyspark.sql.functions import *

orders_df = (
    orders_df
    .select(
        col("order_id").cast("int"),
        col("customer_id").cast("int"),
        col("order_date").cast("date"),
        col("status").cast("string"),
        col("updated_at").cast("timestamp")
    )
    .dropDuplicates(["order_id"])
    .fillna({"status": "unknown"})
    .withColumn("silver_loaded_at", current_timestamp())
)

# COMMAND ----------

# Silver Transformations (Spark Connect Safe) - Order Items
order_items_df = (
    order_items_df
    .select(
        col("order_item_id").cast("int"),
        col("order_id").cast("int"),
        col("product_id").cast("int"),
        col("quantity").cast("int"),
        col("created_at").cast("timestamp")
    )
    .dropDuplicates(["order_item_id"])
    .withColumn("silver_loaded_at", current_timestamp())
)


# COMMAND ----------

# Silver Transformations (Spark Connect Safe) - Payments
#payments_df = None
payments_df = (
    payments_df
    .select(
        col("payment_id").cast("int"),
        col("order_id").cast("int"),
        col("amount").cast("double"),
        col("method").cast("string"),
        col("paid_at").cast("timestamp"),
        col("updated_at").cast("timestamp"),
        col("ingest_date").cast("date")
    )
    .dropDuplicates(["payment_id"])
    .withColumn("silver_loaded_at", current_timestamp())
)

payments_df.write.format("delta").mode("overwrite").save(f"{silver_base}/payments")


# COMMAND ----------

# Silver Transformations (Spark Connect Safe) - Customers
customers_df = (
    customers_df
    .select(
        col("customer_id").cast("int"),
        col("customer_name").cast("string"),
        col("email").cast("string"),
        col("city").cast("string"),
        col("signup_date").cast("date"),
        col("updated_at").cast("timestamp"),
        col("ingest_date").cast("date")
    )
    .dropDuplicates(["customer_id"])
    .withColumn("silver_loaded_at", current_timestamp())
)

# COMMAND ----------

# Silver Transformations (Spark Connect Safe) - Products
products_df = (
    products_df
    .select(
        col("product_id").cast("int"),
        col("product_name").cast("string"),
        col("category").cast("string"),
        col("unit_price").cast("double"),
        col("updated_at").cast("timestamp"),
        col("ingest_date").cast("date")
    )
    .dropDuplicates(["product_id"])
    .withColumn("silver_loaded_at", current_timestamp())
)



# COMMAND ----------

spark.conf.set(  "fs.azure.account.key.atliqdatalake.dfs.core.windows.net",  "<KEY>")
#spark.conf.get("fs.azure.account.key.atliqdatalake.dfs.core.windows.net")

# COMMAND ----------

#orders_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/orders")
order_items_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/order_items")
payments_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/payments")
customers_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/customers")
products_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/products")


# COMMAND ----------

# Write Silver Delta Tables
orders_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.orders")
#orders_df.write.format("delta").mode("overwrite").save(f"{silver_base}/orders")
order_items_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.order_items")
payments_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.payments")
customers_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.customers")
products_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.products")

# COMMAND ----------

dim_customer_df = spark.read.table("gold_gold.dim_customer")
dim_customer_df.coalesce(1).write.mode("overwrite").parquet("abfss://gold@atliqdatalake.dfs.core.windows.net/fabric_export/dim_customer/")
dim_date_df = spark.read.table("gold_gold.dim_date")
dim_date_df.coalesce(1).write.mode("overwrite").parquet("abfss://gold@atliqdatalake.dfs.core.windows.net/fabric_export/dim_date/")
dim_product_df = spark.read.table("gold_gold.dim_product")
dim_product_df.coalesce(1).write.mode("overwrite").parquet("abfss://gold@atliqdatalake.dfs.core.windows.net/fabric_export/dim_product/")
fact_orders_df = spark.read.table("gold_gold.fact_orders")
fact_orders_df.coalesce(1).write.mode("overwrite").parquet("abfss://gold@atliqdatalake.dfs.core.windows.net/fabric_export/fact_orders/")


# COMMAND ----------


# Register Silver Tables (Unity Catalog or Hive)
'''
spark.sql("""CREATE SCHEMA IF NOT EXISTS atliq_silver;""")

spark.sql(f"""CREATE TABLE IF NOT EXISTS atliq_silver.orders USING delta LOCATION '{silver_base}/orders';""")
spark.sql(f"""CREATE TABLE IF NOT EXISTS atliq_silver.order_items USING delta LOCATION '{silver_base}/orders';""")
spark.sql(f"""CREATE TABLE IF NOT EXISTS atliq_silver.payments USING delta LOCATION '{silver_base}/orders';""")
spark.sql(f"""CREATE TABLE IF NOT EXISTS atliq_silver.customers USING delta LOCATION '{silver_base}/orders';""")
spark.sql(f"""CREATE TABLE IF NOT EXISTS atliq_silver.products USING delta LOCATION '{silver_base}/orders';""")
spark.sql(f"""CREATE TABLE IF NOT EXISTS atliq_silver.orders USING delta LOCATION '{silver_base}/orders';""")
'''


'''
# Option 2: Run SQL from Unity Catalog Query Editor (Databricks → SQL → Query Editor → New Query)
CREATE TABLE IF NOT EXISTS atliq_silver.orders USING delta LOCATION 'abfss://silver@<storage-account>.dfs.core.windows.net/orders';

SELECT * FROM atliq_silver.orders LIMIT 10;
SELECT * FROM atliq_silver.order_items LIMIT 10;
SELECT * FROM atliq_silver.payments LIMIT 10;
SELECT * FROM atliq_silver.customers LIMIT 10;
SELECT * FROM atliq_silver.products LIMIT 10;
'''

