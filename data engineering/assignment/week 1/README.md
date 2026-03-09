# Week 1 Assignment – AWS Data Foundations & Cloud ETL

**London Success Academy | Data Engineering Programme**<br>
**Data-SPARK Mentorship – Venkat Potamsetti**

---

## Project Overview

This project demonstrates a beginner-friendly **cloud data engineering pipeline** built entirely using AWS services — no servers to manage, no complex code to write.

**The Business Scenario:**
You are a data engineer at **UrbanNest Property Analytics Ltd**, a London-based property startup. The company received a housing dataset and needs analysts to query it using SQL. Your job is to build the pipeline that makes that possible.

**What this pipeline does:**

- Uploads raw housing data to Amazon S3 (cloud storage)
- Automatically detects the dataset structure using AWS Glue Crawler
- Stores metadata in the Glue Data Catalog (a searchable index)
- Cleans and converts CSV data into optimised Parquet format using AWS Glue ETL
- Enables analysts to query the data using plain SQL through Amazon Athena

This simulates a real-world **serverless ETL pipeline** used in modern data engineering teams.

---

## Technologies Used

| Tool | Purpose |
|------|---------|
| Amazon S3 | Cloud storage for raw and processed data |
| AWS Glue Crawler | Automatically detects schema from raw files |
| AWS Glue Data Catalog | Stores table metadata so tools can find it |
| AWS Glue ETL (Visual ETL) | Transforms CSV data into Parquet format |
| Amazon Athena | Runs SQL queries directly on S3 data |
| VS Code | Local code editing and file management |
| GitHub | Version control and portfolio showcase |

---

## Dataset

The dataset contains housing market information used to analyse property price patterns.

**File location:**

```
house_prices.csv
```

**Columns:**

| Column | Description |
|--------|-------------|
| `rooms` | Average number of rooms per property |
| `distance` | Distance from employment hubs |
| `value` | Median property value |

**Example data:**

| rooms | distance | value |
|-------|----------|-------|
| 6.575 | 4.09 | 24.0 |
| 6.421 | 4.9671 | 21.6 |
| 7.185 | 4.9671 | 34.7 |
| 6.998 | 6.0622 | 33.4 |
| 7.147 | 6.0622 | 36.2 |

The dataset has **506 rows** of real housing data.

---

## Pipeline Architecture

```
house_prices.csv  (local dataset)
        │
        ▼
Amazon S3 – raw folder
s3://urban-nest-data-lake-daniel-2026/raw/house_prices.csv
        │
        ▼
AWS Glue Crawler  (scans file, detects columns and data types)
        │
        ▼
Glue Data Catalog  (stores table metadata – database: urban_nest_db)
        │
        ▼
AWS Glue ETL Job  (reads catalog, removes nulls, converts to Parquet)
        │
        ▼
Amazon S3 – processed folder
s3://urban-nest-data-lake-daniel-2026/processed/
        │
        ▼
Amazon Athena  (SQL queries on processed data)
```

> **Serverless** means none of these services require you to set up or manage a server. AWS handles all the infrastructure automatically.

---

## Project Workflow

### Step 1 – Upload Raw Data to Amazon S3

The raw CSV dataset was uploaded into an Amazon S3 bucket inside the `raw/` folder.

**S3 path:**
```
s3://urban-nest-data-lake-daniel-2026/raw/house_prices.csv
```

**What is S3?** Think of it as a cloud hard drive. Files stored here can be accessed by other AWS services like Glue and Athena.

**Screenshot:**

![S3 Upload](images/Screenshot_1_S3_File_Upload.png)

---

### Step 2 – Create Glue Database

A Glue database was created to act as a container for the dataset metadata.

**Database name:**
```
urban_nest_db
```

**What is a Glue database?** It is not a database in the traditional sense — it is a logical grouping of table metadata inside the Glue Data Catalog.

**Screenshot:**

![Glue Database](images/Screenshot_2_Glue_Database_Created.png)

---

### Step 3 – Run the Glue Crawler

A Glue Crawler was created and pointed at the raw S3 folder. It scanned the CSV file and automatically created a table in the Data Catalog.

| Detail | Value |
|--------|-------|
| **Crawler name** | `urban-nest-house-crawler` |
| **Data source** | `s3://urban-nest-data-lake-daniel-2026/raw/` |
| **Output database** | `urban_nest_db` |
| **Crawler status** | Succeeded |

**What does a crawler do?** It reads your file, figures out the column names and data types automatically, and registers a queryable table — no manual schema definition needed.

**Screenshot:**

![Crawler Completed](images/Screenshot_3_Crawler_Completed.png)

---

### Step 4 – Verify Table Schema in Glue Data Catalog

After the crawler ran, the table schema was verified inside the Glue Data Catalog.

**Columns discovered automatically:**

| Column | Data Type |
|--------|-----------|
| rooms | double |
| distance | double |
| value | double |

**Screenshot:**

![Glue Table Schema](images/Screenshot_4_Glue_Table_Schema.png)

---

### Step 5 – Query Data Using Amazon Athena

Amazon Athena was used to run SQL queries directly on the catalogued data in S3.

**Example query 1 — Get average property value:**
```sql
SELECT AVG(value)
FROM urban_nest_db.house_prices;
```

**Example query 2 — Average value grouped by rooms:**
```sql
SELECT rooms, AVG(value)
FROM urban_nest_db.house_prices
GROUP BY rooms;
```

**What is Athena?** It lets analysts run SQL queries on files stored in S3 without needing a database server. You only pay per query, making it very cost-efficient.

**Screenshot:**

![Athena Query Result](images/Screenshot_5_Athena_Query_Result.png)

---

### Step 6 – Build and Run the Glue ETL Job

A Glue Visual ETL job was created to:
1. Read data from the Glue Data Catalog
2. Remove any null/empty rows
3. Save the cleaned data as **Parquet** format to the processed S3 folder

**Output location:**
```
s3://urban-nest-data-lake-daniel-2026/processed/
```

**What is Parquet?** It is a compressed, columnar file format that is much faster and cheaper to query than CSV — the industry standard for data lakes.

**Screenshot:**

![Glue ETL Job](images/Screenshot_6_Glue_ETL_Job_Success.png)

---

### Step 7 – Verify Processed Data in S3

The transformed Parquet file was confirmed inside the `processed/` folder in S3.

**Screenshot:**

![Processed Data in S3](images/Screenshot_7_S3_Processed_Parquet.png)

---

## Project Folder Structure

```
Week 1/
│
├── house_prices.csv              ← Raw dataset (506 rows of housing data)
│
├── images/
│   ├── Screenshot_1_S3_File_Upload.png
│   ├── Screenshot_2_Glue_Database_Created.png
│   ├── Screenshot_3_Crawler_Completed.png
│   ├── Screenshot_4_Glue_Table_Schema.png
│   ├── Screenshot_5_Athena_Query_Result.png
│   ├── Screenshot_6_Glue_ETL_Job_Success.png
│   └── Screenshot_7_S3_Processed_Parquet.png
│
├── architecture.md               ← Detailed pipeline architecture notes
├── submission_notes.md           ← Step-by-step summary of what was done
├── Week1_Data_Foundations_Cloud_ETL_LSA.pdf  ← Original assignment brief
└── README.md                     ← This file
```

---

## Week 1 Deliverables

The following deliverables were completed as required by the assignment brief:

| Deliverable | Status | Evidence |
|-------------|--------|----------|
| AWS Glue crawler screenshot | Done | `images/Screenshot_3_Crawler_Completed.png` |
| Glue job workflow | Done | `images/Screenshot_6_Glue_ETL_Job_Success.png` |
| Athena query results | Done | `images/Screenshot_5_Athena_Query_Result.png` |
| Documentation of pipeline architecture | Done | `architecture.md` |

---

## Key Learning Outcomes

Through this assignment I learned how to:

- Build a basic **data lake** using Amazon S3 with a raw and processed layer
- Use **AWS Glue Crawler** to automatically detect dataset schema without writing code
- Use the **Glue Data Catalog** to register and manage dataset metadata
- Build a **serverless ETL pipeline** using Glue Visual ETL
- Convert raw **CSV data into Parquet format** for optimised cloud storage
- Query cloud data using **Amazon Athena SQL** to generate business insights
- Apply the **Data-SPARK framework**: structured thinking, pipeline design, and documentation discipline

---

## Glossary — Key Terms for Beginners

| Term | Plain English Explanation |
|------|--------------------------|
| **S3 Bucket** | A cloud folder/hard drive on AWS for storing files |
| **Data Lake** | A central storage location for raw and processed data in the cloud |
| **AWS Glue** | AWS service for discovering, cataloguing, and transforming data |
| **Crawler** | A bot that reads your file and figures out its structure automatically |
| **Data Catalog** | A searchable index of all your datasets — like a library catalogue |
| **ETL Job** | A process that Extracts, Transforms, and Loads data (cleans and moves it) |
| **Parquet** | A faster, compressed file format — much more efficient than CSV for querying |
| **Athena** | AWS service that lets you run SQL queries on S3 files — no database server needed |
| **Serverless** | Cloud services that run without you needing to manage any servers |
| **Schema** | The structure of a dataset — column names and their data types |

---

## Author

**Name:** Daniel Jude<br>
**Programme:** London Success Academy — Data Engineering<br>
**Assignment:** Week 1 — Data Foundations & Cloud ETL
