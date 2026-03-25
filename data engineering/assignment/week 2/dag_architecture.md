# DAG Architecture – MarketFlow Property Intelligence

## Overview

| Detail | Value |
|--------|-------|
| DAG name | marketflow_daily_pipeline |
| Schedule | Daily at 06:00 UTC |
| Company | MarketFlow Property Intelligence |
| Purpose | Automate daily property data ingestion, transformation, and analytics |

---

## How Week 1 Connects to Week 2

In Week 1, I built the pipeline manually — uploading data, running Glue, and querying with Athena. Week 2 asks the question: how can this run automatically every day without anyone pressing a button?

The answer is a DAG. Instead of manually triggering each step, a DAG controls the order of tasks and runs the whole pipeline on a schedule.

| Week 1 Tool | Week 2 Role |
|-------------|-------------|
| Amazon S3 | Raw data storage — where daily files land |
| AWS Glue | ETL transformation — runs automatically as a DAG task |
| Amazon Athena | Analytics query — triggered at the end of the pipeline |
| Parquet | Output format — produced by the transform task |

---

## DAG Architecture Diagram

![DAG Pipeline Architecture](images/dag_pipeline_architecture.png)

---

## Pipeline Flow

```
New CSV arrives in Amazon S3
        ↓
task_1_validate_data
        ↓
task_2_clean_data
        ↓
task_3_transform_dataset
        ↓
task_4_store_parquet
        ↓
task_5_trigger_analytics
```

---

## Task Node Descriptions

### task_1_validate_data
Checks the incoming daily CSV file for errors before anything else runs. Validates for null values, duplicate records, and data format issues. If validation fails, the pipeline stops — no bad data gets through.

### task_2_clean_data
Removes invalid records, duplicates, and rows with missing values. Standardises column formatting so the data is consistent before transformation.

### task_3_transform_dataset
Applies business logic to the cleaned data using AWS Glue ETL. Converts raw property records into a structured format suitable for analytics.

### task_4_store_parquet
Writes the transformed dataset to the S3 processed folder in Parquet format. Parquet is a compressed, columnar format that makes Athena queries faster and cheaper.

**Output path:**
```
s3://urban-nest-data-lake-daniel-2026/processed/
```

### task_5_trigger_analytics
Refreshes the Athena analytics tables so analysts have access to the latest data immediately after the pipeline completes.

---

## Task Dependencies

| Task | Depends On | Reason |
|------|-----------|--------|
| task_2_clean_data | task_1_validate_data | Cannot clean data that has not been validated |
| task_3_transform_dataset | task_2_clean_data | Cannot transform data that has not been cleaned |
| task_4_store_parquet | task_3_transform_dataset | Cannot store data that has not been transformed |
| task_5_trigger_analytics | task_4_store_parquet | Cannot query data that has not been stored |

The pipeline is **linear** — each step must succeed before the next begins.
