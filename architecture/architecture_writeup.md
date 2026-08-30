## **AtliQ Commerce — End‑to‑End Data Architecture**

AtliQ Commerce uses a modern, scalable data architecture designed to support daily operations (OLTP) and analytical reporting (OLAP) through a clean separation of responsibilities and a nightly synchronization pipeline.

### **1. OLTP Layer — Operational Database (Azure SQL DB)**  
The OLTP system stores real‑time transactional data for customers, orders, order items, products, and payments.  
It follows a **3NF normalized schema** optimized for fast inserts and updates.  
A daily simulator generates new transactions to keep the system active for ingestion.

### **2. Ingestion Layer — Azure Data Factory (ADF)**  
ADF performs metadata‑driven ingestion using an ETL control table.  
It extracts OLTP tables and external CSV files (marketing spend, supplier price list) and loads them into **Azure Data Lake Storage Gen2 (ADLS)**.  
ADF uses **full loads** for static tables and **incremental loads** for transactional tables.

### **3. Storage Layer — ADLS Gen2 (Bronze Zone)**  
Raw data lands in the Bronze zone in its original format.  
This zone acts as the immutable source of truth for downstream processing.

### **4. Transformation Layer — Databricks (Silver & Gold)**  
Databricks processes Bronze data into clean, analytics‑ready tables.

- **Silver Layer:** Standardized, cleaned, deduplicated tables.  
- **Gold Layer:** Business‑ready fact and dimension tables (dim_customer, dim_product, fact_orders).

Databricks jobs run nightly, orchestrated via the Jobs UI, and export Gold tables as **single‑file Parquet** for Fabric.

### **5. Semantic Layer — Microsoft Fabric Lakehouse**  
Fabric Lakehouse imports the Gold Parquet files and exposes them as tables.  
A semantic model is built on top of these tables, defining relationships and measures required for reporting.

### **6. Reporting Layer — Power BI**  
Power BI connects directly to the Fabric Lakehouse semantic model.  
The final dashboard answers the four business questions:

- Revenue trends  
- Top customers  
- Product performance  
- Marketing effectiveness  

### **7. Nightly Sync — End‑to‑End Flow**  
Every night:

1. OLTP receives new transactions  
2. ADF ingests data into ADLS Bronze  
3. Databricks transforms Bronze → Silver → Gold  
4. Databricks exports Gold tables to ADLS  
5. Fabric Lakehouse refreshes Parquet tables  
6. Power BI refreshes the semantic model and dashboard