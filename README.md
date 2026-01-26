# 🛒 E-Commerce End-to-End Data Pipeline 
### *Modern Data Stack (ELT) on Google Cloud Platform*

---

## 📌 Project Overview
This project demonstrates a full-cycle **Modern Data Stack (MDS)** architecture. It automates the process of transforming raw, messy e-commerce data into structured, analytics-ready insights. The pipeline follows the **ELT (Extract, Load, Transform)** pattern, leveraging cloud-native tools to ensure scalability and reliability.

**Key Objectives:**
* Automate data ingestion from local/source to **Google BigQuery**.
* Implement data modeling using **dbt** (Data Build Tool) to create a Star Schema.
* Ensure data quality through automated testing.
* Visualize business KPIs such as Monthly Revenue, Customer Growth, and Top Product Categories.

---

## 🏗️ Architecture
The system architecture is designed with modularity in mind:

1.  **Extract & Load (EL):** Python script to ingest raw CSV data into **BigQuery (Raw Layer)**.
2.  **Transform (T):** Modular SQL modeling using **dbt** to create Staging, Intermediate, and Mart layers.
3.  **Orchestration:** **GitHub Actions** for scheduling and CI/CD.
4.  **Visualization:** **Looker Studio** for dynamic business dashboards.

---

## 🛠️ Tech Stack
| Category | Tool | Description |
| :--- | :--- | :--- |
| **Cloud Warehouse** | **Google BigQuery** | Primary data storage and compute engine. |
| **Data Transformation**| **dbt (Cloud/Core)** | For modular SQL modeling and documentation. |
| **Language** | **Python & SQL** | Core languages for ingestion and transformation. |
| **Orchestration** | **GitHub Actions** | Automating pipeline runs and testing. |
| **Visualization** | **Looker Studio** | BI tool for creating interactive dashboards. |
| **Infrastructure** | **Docker** | Ensuring a consistent environment for local development. |

---

## 🚀 Pipeline Details

### 1. Data Ingestion (Python)
The ingestion script (`scripts/upload_to_bq.py`) handles:
* Connecting to Google Cloud using Service Account credentials.
* Schema auto-detection for raw CSV files.
* Loading data into a `raw_data` dataset in BigQuery.

### 2. Data Modeling (dbt)
The transformation logic is organized into three distinct layers:
* **Staging Layer:** Cleaning raw column names, casting data types, and handling duplicates.
* **Intermediate Layer:** Joining entities (e.g., combining `orders` with `payments`).
* **Mart Layer:** Final **Fact** and **Dimension** tables (e.g., `fct_orders`, `dim_customers`) optimized for BI tools.

### 3. Data Quality Assurance
* **Generic Tests:** Checking for `unique` keys and `not_null` values in critical columns.
* **Singular Tests:** Custom SQL tests to ensure business logic consistency (e.g., total_amount > 0).

---

## 📂 Project Structure
```bash
.
├── dbt_project/          # dbt models and configurations
│   ├── models/
│   │   ├── staging/      # Layer 1: Data cleaning & Type casting
│   │   ├── intermediate/ # Layer 2: Business logic & Joins
│   │   └── marts/        # Layer 3: Analytics-ready Fact/Dim tables
│   ├── tests/            # Custom data quality tests
│   └── dbt_project.yml
├── scripts/              # Python ingestion scripts
│   └── upload_to_bq.py
├── .github/workflows/    # CI/CD and Automation schedules
├── requirements.txt      # Project dependencies
└── README.md
```
---
## 🛠️ Installation & Setup
1. Clone the Repository:

```bash
git clone [https://github.com/your-username/ecommerce-data-pipeline.git](https://github.com/your-username/ecommerce-data-pipeline.git)
```

2. Download datatset by running loaddataset.py file
3. Run Ingestion:
```bash
python scripts/upload_to_bq.py
```
4. Execute dbt Models:
```bash
cd dbt_project
dbt build
```