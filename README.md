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

## **CI/CD and Reliability Layer — GitHub Actions + dbt**

To treat the data platform as a production-grade system, the project is managed through GitHub and automated CI/CD validation.

### **Source Control**
- All project assets are stored in GitHub
- Version controlled components include:
  - Azure Data Factory pipeline JSON files
  - Databricks notebooks
  - dbt project files
  - Documentation and architecture diagrams
- Changes are committed through feature branches and merged via Pull Requests

### **Continuous Integration (CI)**
- Implemented using GitHub Actions
- Automatically runs whenever:
  - A Pull Request is created
  - Changes are pushed to the main branch
- Uses Databricks connection details stored securely as GitHub Secrets

### **Automated dbt Validation**
During every CI run:

1. Checkout repository source code
2. Install Python and dbt-databricks
3. Generate a temporary CI profile
4. Validate Databricks connectivity
5. Execute `dbt deps`
6. Execute `dbt build`
7. Execute `dbt test`

This ensures:

- Models compile successfully
- Data quality tests pass
- Relationships remain valid
- Broken code cannot be merged unnoticed

### **CI Environment Isolation**
- CI executes against a dedicated validation schema
- Production Gold objects are never modified during validation
- Environment-specific settings are managed through variables and secrets

### **Reliability Controls**
- dbt tests run automatically on every Pull Request
- Data quality failures stop the pipeline
- GitHub Actions provides build history and execution logs
- Nightly orchestration is designed to be idempotent
- Fact and dimension loads produce consistent results across reruns

### **Reliability Verification**
The platform validates reliability through:

- Successful dbt build execution
- Automated schema validation
- Automated relationship testing
- Automated not-null testing
- Automated uniqueness testing
- Nightly job monitoring
- Row-count and revenue verification after repeated pipeline executions

---

## **Updated Nightly Sync Workflow**

1. OLTP receives new transactions
2. ADF ingests OLTP + external data into ADLS Bronze
3. Databricks transforms Bronze → Silver
4. dbt builds and tests Gold models
5. Gold tables are published for analytics
6. Fabric Lakehouse refreshes tables
7. Power BI refreshes the semantic model and dashboard
8. GitHub Actions validates future code changes through CI

This ensures the business always sees **fresh, accurate, tested, and reliable data**.

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
- **dbt (Data Build Tool)** — Gold layer transformations and testing
- **GitHub Actions** — CI/CD automation and validation

---

## **Purpose of This Architecture**
- Keep OLTP fast and isolated from analytics  
- Provide a clean, governed data pipeline  
- Deliver reliable nightly insights  
- Support scalable reporting for business teams