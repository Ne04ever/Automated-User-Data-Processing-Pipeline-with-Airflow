# 🛠️ User Data ETL Pipeline with Apache Airflow

This project is an ETL (Extract, Transform, Load) pipeline built using **Apache Airflow**. It fetches random user data from a public API, processes it using **Pandas**, and stores the final structured data into a **PostgreSQL** database.

---

## 🚀 Pipeline Overview

### 📊 Flow of the DAG

1. **Check API Availability** using `HttpSensor`
2. **Extract** user data from `https://randomuser.me/api/` using `SimpleHttpOperator`
3. **Process** nested JSON into flat tabular format with `Pandas`
4. **Store** the processed data into PostgreSQL using `PostgresHook` and the `COPY` command

---

## 🧩 Components

### 🐘 PostgreSQL Table

The pipeline creates the following table if it doesn't already exist:

```sql
CREATE TABLE IF NOT EXISTS users (
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  country TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL
);

## Tasks
| Task ID            | Description                                           |
| ------------------ | ----------------------------------------------------- |
| `create_table`     | Creates `users` table in PostgreSQL                   |
| `is_api_available` | Checks if the user API is available                   |
| `extract_user`     | Fetches one random user via GET request               |
| `process_user`     | Normalizes nested JSON into CSV format                |
| `store_user`       | Inserts processed CSV data into PostgreSQL using COPY |


