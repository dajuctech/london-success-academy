---
title: "Week 2 Assignment – Data Pipeline Orchestration"
author: "Daniel Jude"
date: "March 2026"
subtitle: "London Success Academy | Data-SPARK Mentorship – Venkat Potamsetti"
geometry: margin=2.5cm
fontsize: 12pt
linestretch: 1.5
colorlinks: true
---

---

## Overview

Week 2 picks up exactly where Week 1 left off. In Week 1 I manually uploaded a CSV to S3, ran a Glue crawler, set up the ETL job, and queried the results in Athena. It worked — but I had to do every step myself. Week 2 asked a question that made me think differently: what happens when you have to do all of that again tomorrow? And the day after that?

That is the real problem MarketFlow Property Intelligence is facing. After UrbanNest merged with another analytics company, the business now receives property data feeds from multiple agencies every single day. Someone running the pipeline manually each morning is not a realistic answer. This week I had to design a DAG — a Directed Acyclic Graph — that automates the entire process on a schedule.

---

## How Week 1 Connects to Week 2

The tools are the same. What changes is how they are controlled.

In Week 1 the pipeline was:

```
CSV → S3 → Glue → Athena
```

Each of those steps needed me to click, wait, and confirm. Week 2 wraps that same pipeline inside an automated workflow that triggers itself at 06:00 UTC every morning without anyone touching it.

| Week 1 Tool | Week 2 Role |
|-------------|-------------|
| Amazon S3 | Raw data storage — where daily files land |
| AWS Glue | ETL transformation — runs automatically as a DAG task |
| Amazon Athena | Analytics query — triggered at the end of the pipeline |
| Parquet | Output format — produced by the transform task |

Once I saw it as the same pipeline just on a timer, the design became a lot clearer.

---

## Task 1 – DAG Structure

A DAG is a workflow map. Each box is a task. The arrows show what needs to happen before the next step can start. The key rule is that you cannot go backwards — a failed task does not automatically retry and you cannot loop back to an earlier step without restarting the whole run.

For MarketFlow I designed five tasks that run in order every day:

| Task | What It Does |
|------|-------------|
| task_1_validate_data | Checks the incoming data for errors before anything else runs |
| task_2_clean_data | Removes bad rows and standardises column formatting |
| task_3_transform_dataset | Applies business logic using AWS Glue ETL |
| task_4_store_parquet | Writes the output to S3 in Parquet format |
| task_5_trigger_analytics | Refreshes Athena so analysts get the latest data |

The pipeline is linear — each step only runs if the one before it succeeded.

---

## Task 2 – DAG Workflow Design

**DAG name:** marketflow_daily_pipeline

**Schedule:** Every day at 06:00 UTC

**DAG diagram:**

![MarketFlow Daily Pipeline DAG](images/dag_pipeline_architecture.png)

**Task dependencies:**

| Task | Depends On | Reason |
|------|-----------|--------|
| task_2_clean_data | task_1_validate_data | Cannot clean unvalidated data |
| task_3_transform_dataset | task_2_clean_data | Cannot transform uncleaned data |
| task_4_store_parquet | task_3_transform_dataset | Cannot store untransformed data |
| task_5_trigger_analytics | task_4_store_parquet | Cannot query data not yet stored |

---

## Pipeline Workflow

### Step 1 – Data Upload

Every morning, property datasets from multiple real estate agencies arrive in the S3 bucket and land in the raw folder. The pipeline waits for these files before doing anything.

```
s3://urban-nest-data-lake-daniel-2026/raw/
```

### Step 2 – Data Validation

The first task runs three quality checks on every file. If any of them fail, the whole pipeline stops right there. I put this first because catching a problem at the entry point is far cheaper than finding corrupted data in the analytics layer later on.

### Step 3 – Data Cleaning

Once the data passes validation, this task removes invalid rows, drops duplicates, and standardises column formatting. By the time this step finishes, the dataset is in a consistent shape ready for transformation.

### Step 4 – Data Transformation

AWS Glue ETL runs the business logic — calculating derived fields, filtering out outliers, and restructuring the data into the format the reporting layer expects. This is the same Glue job I built in Week 1, now triggered automatically instead of manually.

### Step 5 – Data Storage

The transformed dataset is written to S3 in Parquet format.

```
s3://urban-nest-data-lake-daniel-2026/processed/
```

Parquet came up in Week 1 and I did not fully appreciate it then. After Week 2 it made more sense — it is columnar, so Athena only reads the specific columns a query needs instead of scanning the whole file. That directly reduces query cost and time.

### Step 6 – Analytics Query

The final task refreshes the Athena analytics tables. When analysts arrive in the morning, they can query the latest data immediately without waiting for anyone on the data team to manually trigger anything.

---

## Task 3 – Validation Logic

Three checks run on every incoming file. All three have to pass before the pipeline continues.

### Check 1 – Null Values

Every row must have a value in the four required fields: `property_id`, `rooms`, `distance`, and `property_value`. A missing value in any of these makes the record unusable for analysis.

```sql
SELECT COUNT(*) AS null_count
FROM property_data
WHERE property_id IS NULL
   OR rooms IS NULL
   OR distance IS NULL
   OR property_value IS NULL;
```

**Pass condition:** null_count = 0

**On failure:** Pipeline stops. Alert sent with the count of null rows and the source filename.

---

### Check 2 – Duplicate Records

Each property should appear only once in a daily feed. If the same property_id appears more than once, it means either the agency sent a duplicate or there was an error in their export.

```sql
SELECT property_id, COUNT(*) AS record_count
FROM property_data
GROUP BY property_id
HAVING COUNT(*) > 1;
```

**Pass condition:** Query returns zero rows

**On failure:** Pipeline stops. Duplicate rows are logged with counts so the team knows exactly which records to investigate.

---

### Check 3 – Data Format Validation

Values have to make sense. A property cannot have zero rooms. Distance cannot be negative. A property_value of zero would mean the data is either wrong or the property was recorded incorrectly.

```sql
SELECT COUNT(*) AS invalid_count
FROM property_data
WHERE rooms <= 0
   OR distance < 0
   OR property_value <= 0;
```

**Pass condition:** invalid_count = 0

**On failure:** Pipeline stops. A sample of the invalid rows is logged so the team can see what went wrong.

---

## Task 4 – Monitoring Strategy

The pipeline running correctly is the expected outcome. What separates a reliable production pipeline from a fragile one is knowing what went wrong, when, and why — before someone else notices.

I designed four alerts for this pipeline.

### Alert 1 – Pipeline Failure Alert

If any task fails, the team needs to know immediately. Waiting until morning standup is too late if the pipeline broke at 06:14.

| Detail | Value |
|--------|-------|
| Alert name | PIPELINE_TASK_FAILURE |
| Trigger | Any task status = FAILED |
| Severity | Critical |
| Notification | Email + Slack to data engineering team |
| Response time | Investigate within 15 minutes |

**Example message:**
> CRITICAL: marketflow_daily_pipeline — task_3_transform_dataset FAILED at 06:14 UTC. Investigate immediately.

**Action:**
1. Check task logs to identify the error
2. Fix the root cause
3. Re-trigger the failed task
4. Document the incident

---

### Alert 2 – Missing Data Alert

If no data file arrives from the agencies by 05:50, there is no point running the pipeline. This alert fires early enough to contact the supplier before the scheduled run.

| Detail | Value |
|--------|-------|
| Alert name | MISSING_DAILY_DATA_FILE |
| Trigger | No new file in S3 raw folder by 05:50 UTC |
| Severity | High |
| Notification | Email to data engineering team and data suppliers |
| Response time | Investigate within 30 minutes |

**Example message:**
> HIGH: No property data file received for today by 05:50 UTC. Pipeline paused. Contact data suppliers.

**Action:**
1. Check if the data supplier had a system issue
2. Request a manual resend if possible
3. If no data arrives by 07:00, skip today's run and notify analysts

---

### Alert 3 – Job Execution Error

A task that is running for three times its normal duration is a sign something has gone wrong even if it has not failed yet. Catching these early prevents one slow task from holding up everything downstream.

| Task | Expected Runtime | Timeout |
|------|-----------------|---------|
| task_1_validate_data | 2 minutes | 10 minutes |
| task_2_clean_data | 5 minutes | 20 minutes |
| task_3_transform_dataset | 10 minutes | 30 minutes |
| task_4_store_parquet | 5 minutes | 20 minutes |
| task_5_trigger_analytics | 3 minutes | 15 minutes |

| Detail | Value |
|--------|-------|
| Alert name | TASK_EXECUTION_TIMEOUT |
| Trigger | Task runtime exceeds threshold |
| Severity | Warning |
| Notification | Slack to data engineering team |
| Response time | Investigate within 30 minutes |

**Example message:**
> WARNING: task_3_transform_dataset has been running for 31 minutes. Expected: 10 minutes. Check for resource issues.

---

### Alert 4 – Data Quality Alert

Sometimes the data passes the validation checks technically but a high percentage of records are still flagged as borderline. If 8% of records are failing format checks, that is a pattern worth investigating even if the pipeline continues.

| Detail | Value |
|--------|-------|
| Alert name | HIGH_INVALID_RECORD_RATE |
| Trigger | More than 5% of records fail any validation check |
| Severity | Warning |
| Notification | Email to data engineering team |
| Response time | Review before next pipeline run |

**Example message:**
> WARNING: 8.2% of records in today's dataset failed format validation. Pipeline continued but data quality review recommended.

**Action:**
1. Review which agency the flagged records came from
2. Contact the agency to flag the data quality issue
3. Monitor the next delivery to see if it repeats

---

## Deliverables Summary

| Deliverable | Status | File |
|-------------|--------|------|
| DAG architecture diagram | Done | dag_architecture.md |
| Pipeline workflow documentation | Done | pipeline_workflow.md |
| Validation logic explanation | Done | validation_logic.md |
| Monitoring strategy | Done | monitoring_plan.md |

---

## What I Learned

The shift from Week 1 to Week 2 was not about learning new tools. It was about thinking differently about the tools I already used. In Week 1 I was asking how do I get this to work. In Week 2 the question was how do I make this work every day without me being involved.

A few things stood out:

The validation step being first is not obvious until you think about what happens if it is not. I had originally sketched the DAG with cleaning happening before validation — it seemed like a natural order. But if you clean data that has not been validated, you are spending compute time on records you might end up rejecting anyway. Validation first means nothing downstream ever touches bad data.

The monitoring section took longer than I expected. Writing out the four alerts made me realise how much can go wrong in a pipeline that looks simple on paper. The DAG diagram is five boxes with arrows. The monitoring plan covers what happens when any of those boxes does not behave as expected — and there are more failure modes than the diagram suggests.

The most useful thing about this week was seeing the full picture. In Week 1 each tool felt separate: S3 is storage, Glue is transformation, Athena is querying. Week 2 showed me how they fit together as a system that runs on its own every morning. That connection changed how I understand what a data pipeline actually is.

---

## Author

**Name:** Daniel Jude

**Programme:** London Success Academy – Data Engineering

**Assignment:** Week 2 – Data Pipeline Orchestration

**Date:** March 2026
