# Databricks notebook source
# MAGIC %md
# MAGIC **This notebook is run only afte gold table/data is created to load into adls gen 2.[](url)**

# COMMAND ----------

spark.conf.set(  "fs.azure.account.key.atliqdatalake.dfs.core.windows.net",  "<KEY>")
#spark.conf.get("fs.azure.account.key.atliqdatalake.dfs.core.windows.net")

# COMMAND ----------

# Read
#orders_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/orders")
#order_items_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/order_items")
#payments_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/payments")
#customers_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/customers")
#products_df = spark.read.format("delta").load("abfss://silver@atliqdatalake.dfs.core.windows.net/products")

# Write Silver Delta Tables
#orders_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.orders")
#order_items_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.order_items")
#payments_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.payments")
#customers_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.customers")
#products_df.write.format("delta").mode("overwrite").saveAsTable("atliq_dbx.silver.products")

# COMMAND ----------

dim_customer_df = spark.read.table("gold_gold.dim_customer")
dim_customer_df.coalesce(1).write.mode("overwrite").parquet("abfss://gold@atliqdatalake.dfs.core.windows.net/fabric_export/dim_customer/")
dim_date_df = spark.read.table("gold_gold.dim_date")
dim_date_df.coalesce(1).write.mode("overwrite").parquet("abfss://gold@atliqdatalake.dfs.core.windows.net/fabric_export/dim_date/")
dim_product_df = spark.read.table("gold_gold.dim_product")
dim_product_df.coalesce(1).write.mode("overwrite").parquet("abfss://gold@atliqdatalake.dfs.core.windows.net/fabric_export/dim_product/")
fact_orders_df = spark.read.table("gold_gold.fact_orders")
fact_orders_df.coalesce(1).write.mode("overwrite").parquet("abfss://gold@atliqdatalake.dfs.core.windows.net/fabric_export/fact_orders/")
