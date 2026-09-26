#  GoogleForm-Medallion-ETL (Prototype)

An End-to-End Data Pipeline prototype designed to process university form data using the **Medallion Architecture** (Bronze, Silver, Gold), loaded into PostgreSQL via Docker, and visualized in Power BI.

---

##  Architecture & Pipeline Flow

1. **Bronze Layer (Raw)**: Ingests raw CSV form submission data directly into PostgreSQL without modifications.
2. **Silver Layer (Cleaned)**: Performs data cleaning, standardizing text formatting, handling missing values, deduplication, and loading into PostgreSQL using **Batch Processing (`%` modulo technique)**.
3. **Gold Layer (Aggregated)**: Calculates business metrics (e.g., total responses, average satisfaction score per faculty) ready for consumption.
4. **Visualization**: Power BI connects to the Gold Layer for reporting and dashboarding.

---

##  Tech Stack

* **Database & Infrastructure**: PostgreSQL 15, Docker Compose
* **Data Processing & ETL**: Python 3, Pandas, SQLAlchemy, Pypsycopg2
* **Visualization Target**: Power BI Desktop
* **Version Control**: Git & GitHub

---

##  How to Run locally

1. **Start PostgreSQL Container**:
   ```bash
   docker-compose up -d
   ```

2. Execute Medallion Pipeline:
  ```bash
  python scripts/etl_bronze.py
  python scripts/etl_silver.py
  python scripts/etl_gold.py
  ```

3. Connect to Power BI:

* Host: localhost:5432
* Database: medallion_db
* Query Table: gold_faculty_summary

