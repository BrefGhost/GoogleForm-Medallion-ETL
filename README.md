# GoogleForm-Medallion-ETL (Prototype)

An End-to-End Data Pipeline prototype designed to process university form data using the **Medallion Architecture** (Bronze, Silver, Gold), loaded into PostgreSQL via Docker, and visualized in Power BI. Includes two ways to orchestrate the pipeline: **Docker Compose** and **Apache Airflow**.

---

## Architecture & Pipeline Flow

1. **Bronze Layer (Raw)**: Ingests raw CSV form submission data directly into PostgreSQL without modifications.
2. **Silver Layer (Cleaned)**: Performs data cleaning, standardizing text formatting, handling missing values, deduplication, and loading into PostgreSQL using **Batch Processing (`%` modulo technique)**.
3. **Gold Layer (Aggregated)**: Calculates business metrics (e.g., total responses, average satisfaction score per faculty) ready for consumption.
4. **Visualization**: Power BI connects to the Gold Layer for reporting and dashboarding.

---

## Tech Stack

* **Database & Infrastructure**: PostgreSQL 15, Docker, Docker Compose
* **Orchestration**: Docker Compose (`depends_on` + health checks) and Apache Airflow 2.10.5 (`DockerOperator`)
* **Data Processing & ETL**: Python 3, Pandas, SQLAlchemy, psycopg2
* **Visualization Target**: Power BI Desktop
* **Version Control**: Git & GitHub

---

## How to Run

### Option 1 — Docker Compose only (fully automated, single command)

Runs Postgres and all three ETL stages as containers, chained with `depends_on: service_completed_successfully` so each stage waits for the previous one to finish:

```bash
docker-compose up --build
```

### Option 2 — Manual (for debugging one stage at a time)

```bash
docker-compose up -d        # start Postgres only
python scripts/etl_bronze.py
python scripts/etl_silver.py
python scripts/etl_gold.py
```

### Option 3 — Apache Airflow (scheduled / monitored orchestration)

The `airflow/` folder runs a separate Airflow 2.10.5 instance that triggers the same bronze/silver/gold Docker images via `DockerOperator`, giving a UI, run history, and retry support on top of the Docker Compose pipeline above.

```bash
cd airflow
cp .env.example .env
docker-compose up airflow-init
docker-compose up -d
```

Open `http://localhost:8080` (user: `airflow` / pass: `airflow`), unpause the `medallion_pipeline` DAG, and trigger it. It runs `bronze_task >> silver_task >> gold_task` against the **same Postgres instance and Docker
