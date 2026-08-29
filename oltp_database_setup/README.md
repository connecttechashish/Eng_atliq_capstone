# **README — OLTP Database Setup (Section 1)**

This folder contains everything needed to spin up the operational database for the AtliQ Commerce project. The OLTP layer is the starting point of the entire pipeline, so the goal here is simple: create a clean, consistent, fully‑seeded transactional database that represents how a real e‑commerce system stores its day‑to‑day activity.

The scripts in this section build the core entities — customers, products, orders, order items, and payments — along with realistic sample data. Once deployed, this database becomes the source for ingestion into Azure Data Factory and eventually flows into the Silver and Gold layers in Databricks.

---

## **📁 What’s inside this folder**

| File | Description |
|------|-------------|
| `01_schema_ddl.sql` | Creates all OLTP tables with proper keys, constraints, and relationships |
| `02_insert_customers.sql` | Loads 40 customer records |
| `03_insert_products.sql` | Loads 25 product records |
| `04_insert_orders.sql` | Inserts 300 orders with timestamps |
| `05_insert_order_items.sql` | Inserts 783 order item rows |
| `06_insert_payments.sql` | Inserts 246 payment transactions |

All scripts are designed to run cleanly on **Azure SQL Database**.

---

## **🧱 Schema Overview**

The OLTP schema follows a simple, normalized structure:

- **customers** – basic customer profile and signup details  
- **products** – product catalog with categories and pricing  
- **orders** – order header information  
- **order_items** – line‑level details for each order  
- **payments** – payment records tied to orders  

Foreign keys ensure referential integrity, and timestamps help simulate real‑world transactional behavior.

---

## **🚀 How to deploy the OLTP database**

1. Connect to your Azure SQL Database using Azure Data Studio or SQL Server Management Studio.
2. Run the schema file first:

   ```sql
   :r 01_schema_ddl.sql
   ```

3. Load the seed data in order:

   ```sql
   :r 02_insert_customers.sql
   :r 03_insert_products.sql
   :r 04_insert_orders.sql
   :r 05_insert_order_items.sql
   :r 06_insert_payments.sql
   ```

4. Validate the row counts:

   ```sql
   SELECT COUNT(*) FROM customers;
   SELECT COUNT(*) FROM products;
   SELECT COUNT(*) FROM orders;
   SELECT COUNT(*) FROM order_items;
   SELECT COUNT(*) FROM payments;
   ```

If all counts match, your OLTP layer is ready for ingestion.