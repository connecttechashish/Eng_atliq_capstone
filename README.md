# **README.md — AtliQ Commerce Architecture**

## **Overview**
AtliQ Commerce uses a modern, cloud‑native data architecture designed to support daily operations (OLTP) and analytical reporting (OLAP). The system separates transactional workloads from analytical workloads and synchronizes them through a nightly pipeline. This ensures fast application performance and reliable business insights.

---

## **Architecture Components**

### **1. OLTP Layer — Azure SQL Database**
- Stores customer, product, order, order item, and payment data  
- Fully normalized (3NF) schema  
- Updated daily using a Python‑based transaction simulator  
- Optimized for inserts, updates, and real‑time operations  
- Source of truth for ingestion

### **2. Ingestion Layer — Azure Data Factory (ADF)**
- Metadata‑driven ingestion using an ETL control table  
- Extracts OLTP tables and external CSV files  
- Supports **full** and **incremental** loads  
- Loads raw data into ADLS Bronze zone  
- Ensures consistent nightly refresh

### **3. Storage Layer — Azure Data Lake Storage Gen2 (ADLS)**
- **Bronze Zone:** Raw data exactly as ingested  
- Acts as the landing zone for all upstream systems  
- Provides durable, scalable storage for downstream processing

### **4. Processing Layer — Databricks**
- Converts Bronze → Silver → Gold  
- **Silver Layer:** Cleaned, standardized, deduplicated tables  
- **Gold Layer:** Business‑ready fact and dimension tables  
- Databricks Jobs orchestrate nightly transformations  
- Gold tables exported as **single‑file Parquet** for Fabric

### **5. Analytics Layer — Microsoft Fabric Lakehouse**
- Imports Gold Parquet files from ADLS  
- Creates Lakehouse tables for semantic modeling  
- Defines relationships and measures for reporting  
- Serves as the analytical foundation for Power BI

### **6. Reporting Layer — Power BI**
- Connects directly to Fabric Lakehouse  
- Provides dashboards answering key business questions:  
  - Revenue trends  
  - Top customers  
  - Product performance  
  - Marketing effectiveness  
- Refreshes nightly after Lakehouse updates

---

## **Nightly Sync Workflow**
1. OLTP receives new transactions  
2. ADF ingests OLTP + external data into ADLS Bronze  
3. Databricks transforms Bronze → Silver → Gold  
4. Databricks exports Gold tables to ADLS as Parquet  
5. Fabric Lakehouse refreshes tables  
6. Power BI refreshes the semantic model and dashboard  

This ensures the business always sees **fresh, accurate, and consistent data**.

---

## **Technologies Used**
- **Azure SQL Database** — OLTP storage  
- **Azure Data Factory** — ingestion pipelines  
- **Azure Data Lake Storage Gen2** — Bronze storage  
- **Databricks** — transformation (Silver/Gold)  
- **Parquet** — export format for Fabric  
- **Microsoft Fabric Lakehouse** — analytical storage  
- **Power BI** — reporting and dashboards  
- **Python** — transaction simulator  
- **SQL** — OLTP schema + Databricks SQL  
- **GitHub** — version control

---

## **Purpose of This Architecture**
- Keep OLTP fast and isolated from analytics  
- Provide a clean, governed data pipeline  
- Deliver reliable nightly insights  
- Support scalable reporting for business teams