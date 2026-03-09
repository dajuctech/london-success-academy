# Architecture Explanation

## Pipeline Flow
1. A raw CSV file (`house_prices.csv`) was prepared locally.
2. The CSV was uploaded into Amazon S3 under the `raw/` folder.
3. AWS Glue Crawler scanned the raw file and created a table in the Glue Data Catalog.
4. AWS Glue ETL Job read the catalog table and transformed the CSV into Parquet format.
5. The processed Parquet file was stored in the `processed/` folder in S3.
6. Amazon Athena was used to query both the catalog table and the processed data.

## Architecture Diagram
CSV file
↓
Amazon S3 (raw)
↓
AWS Glue Crawler
↓
Glue Data Catalog
↓
AWS Glue ETL Job
↓
Amazon S3 (processed Parquet)
↓
Amazon Athena

## Why this matters
This project demonstrates a basic serverless AWS data pipeline and shows how raw data can be ingested, cataloged, transformed, and queried for analytics.