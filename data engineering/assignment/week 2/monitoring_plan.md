# Monitoring Strategy

## Overview

Monitoring ensures that the pipeline runs reliably every day and that errors are detected and acted on quickly. MarketFlow analysts depend on fresh data every morning — without monitoring, a silent failure at 6am could go unnoticed until mid-morning, by which time analysts may have already made decisions on stale data.

---

## Alert 1 – Pipeline Failure Alert

**What it monitors:**
Any DAG task that exits with an error or non-zero status code.

**How it is detected:**
Apache Airflow marks the task as FAILED and triggers a notification immediately.

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

## Alert 2 – Missing Data Alert

**What it monitors:**
Whether the daily property data file arrived in S3 before the pipeline is due to start.

**How it is detected:**
A pre-check runs at 05:50 UTC. If no new file exists in the raw S3 folder, the pipeline is paused and an alert fires.

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
3. If no data arrives, skip today's run and notify analysts

---

## Alert 3 – Job Execution Error

**What it monitors:**
Tasks that are running but taking significantly longer than expected — a sign that something is wrong even if the task has not failed yet.

| Task | Expected Runtime | Timeout Threshold |
|------|-----------------|-------------------|
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

## Alert 4 – Data Quality Alert

**What it monitors:**
The number of invalid records flagged during the validation step. Even if validation technically passes, a high percentage of flagged records is a warning sign.

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

## Monitoring Summary

| Alert | Trigger | Severity | Response Time |
|-------|---------|----------|---------------|
| Pipeline Failure | Any task FAILED | Critical | 15 minutes |
| Missing Data | No S3 file by 05:50 UTC | High | 30 minutes |
| Job Execution Error | Task exceeds timeout | Warning | 30 minutes |
| Data Quality Alert | >5% invalid records | Warning | Before next run |
