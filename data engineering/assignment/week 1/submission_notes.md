# Submission Notes

## Step 1 - Prepared the dataset
I created the `house_prices.csv` dataset locally and stored it in the `data/` folder.

## Step 2 - Uploaded raw data to Amazon S3
I created an S3 bucket and uploaded the CSV file into the `raw/` folder.

## Step 3 - Created the Glue database
I created a Glue database called `urban_nest_db`.

## Step 4 - Ran the Glue crawler
I created and ran a Glue crawler to scan the raw dataset in S3. The crawler generated a table called `raw`.

## Step 5 - Verified schema in Glue Data Catalog
I confirmed that the table schema contained the expected columns:
- rooms
- distance
- value

## Step 6 - Queried the data in Athena
I queried the table using Athena to confirm the data was accessible and correct.

## Step 7 - Built the ETL job
I used Glue Visual ETL to read from the Glue Data Catalog and write processed output to S3 in Parquet format.

## Step 8 - Verified processed output
I confirmed that the processed Parquet file was successfully written into the `processed/` folder in S3.

## Step 9 - Queried processed data
I used Athena to query the processed dataset and confirmed that the pipeline worked end-to-end.