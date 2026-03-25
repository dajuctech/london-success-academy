# Pipeline Workflow Documentation

## Overview

This pipeline automates the daily processing of property data received from multiple real estate agencies at MarketFlow Property Intelligence.

The workflow is controlled using a Directed Acyclic Graph (DAG) that runs every day at 06:00 UTC. Each step must complete successfully before the next one begins.

![DAG Pipeline Architecture](images/dag_pipeline_architecture.png)

---

## Pipeline Steps

### Step 1 – Data Upload

Property datasets arrive daily in an Amazon S3 bucket from multiple real estate agencies. The raw files land in the `raw/` folder and wait for the pipeline to begin at 06:00 UTC.

**S3 path:**
```
s3://urban-nest-data-lake-daniel-2026/raw/
```

---

### Step 2 – Data Validation (task_1_validate_data)

The pipeline validates the incoming dataset to ensure data quality before any processing happens. Three checks are performed:

- Null value check — ensures no required fields are missing
- Duplicate record check — ensures no property record appears more than once
- Data format check — ensures values are within realistic ranges

If any check fails, the pipeline stops immediately and an alert is sent to the data engineering team.

---

### Step 3 – Data Cleaning (task_2_clean_data)

Invalid records, duplicates, and rows with missing values are removed. Column formatting is standardised across all fields. The output of this step is a clean, consistent dataset ready for transformation.

---

### Step 4 – Data Transformation (task_3_transform_dataset)

AWS Glue ETL applies business logic to the cleaned data. This includes:

- Calculating derived fields
- Filtering out outlier values
- Structuring the data into the analytical format expected by the reporting layer

This step is where raw property records become useful business data.

---

### Step 5 – Data Storage (task_4_store_parquet)

The transformed dataset is saved to the S3 processed folder in **Parquet format**.

Parquet is the industry-standard format for data lakes because it is:
- Compressed — uses less storage than CSV
- Columnar — Athena only reads the columns it needs, reducing query cost
- Fast — significantly quicker to query than raw CSV

**Output path:**
```
s3://urban-nest-data-lake-daniel-2026/processed/
```

---

### Step 6 – Analytics Query (task_5_trigger_analytics)

Once the processed Parquet file is stored, the pipeline triggers a refresh of the Athena analytics tables. Analysts can immediately query the latest data using SQL through Amazon Athena without any manual steps.

---

## End-to-End Flow Summary

| Step | Task | Tool Used |
|------|------|-----------|
| 1 | Data arrives in S3 | Amazon S3 |
| 2 | Validate dataset | Custom validation checks |
| 3 | Clean dataset | AWS Glue |
| 4 | Transform dataset | AWS Glue ETL |
| 5 | Store as Parquet | Amazon S3 |
| 6 | Trigger analytics | Amazon Athena |
