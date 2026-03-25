# Week 2 Assignment – Data Pipeline Orchestration

**London Success Academy | Data Engineering Programme**<br>
**Data-SPARK Mentorship – Venkat Potamsetti**

---

## Project Scenario

UrbanNest Property Analytics (from Week 1) has merged with MarketFlow Property Intelligence. The company now receives **daily property data updates from multiple real estate agencies**.

Running data pipelines manually every day is no longer efficient. The company needs an **automated workflow** — a Directed Acyclic Graph (DAG) — that runs the pipeline on a schedule without any manual intervention.

My job this week is to **design and document that DAG**.

---

## How Week 1 Connects to Week 2

In Week 1, I built the pipeline manually:

```
CSV → S3 → Glue → Athena
```

Week 2 automates that same pipeline so it runs every day at 06:00 UTC without anyone pressing a button.

| Week 1 Tool | Week 2 Role |
|-------------|-------------|
| Amazon S3 | Raw data storage — where daily files land |
| AWS Glue | ETL transformation — runs automatically as a DAG task |
| Amazon Athena | Analytics query — triggered at the end of the pipeline |
| Parquet | Output format — produced by the transform task |

---

## DAG Workflow

The pipeline performs these tasks in order every day:

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

Each task only runs if the previous one succeeds. If any task fails, the pipeline stops and an alert is triggered.

---

## Pipeline Architecture

![DAG Pipeline Architecture](images/dag_pipeline_architecture.png)

---

## Task Descriptions

| Task | What It Does |
|------|-------------|
| task_1_validate_data | Runs data quality checks — null values, duplicates, format |
| task_2_clean_data | Removes invalid rows, standardises formatting |
| task_3_transform_dataset | Applies business logic using AWS Glue ETL |
| task_4_store_parquet | Writes output to S3 processed folder as Parquet |
| task_5_trigger_analytics | Refreshes Athena analytics tables for analysts |

---

## Week 2 Deliverables

| Deliverable | Status | File |
|-------------|--------|------|
| DAG architecture diagram | Done | `dag_architecture.md` |
| Pipeline workflow documentation | Done | `pipeline_workflow.md` |
| Validation logic explanation | Done | `validation_logic.md` |
| Monitoring strategy | Done | `monitoring_plan.md` |

---

## Folder Structure

```
Week 2/
│
├── dag_architecture.md          ← DAG design, diagram, task descriptions
├── pipeline_workflow.md         ← Step-by-step pipeline workflow
├── validation_logic.md          ← Three validation checks with SQL
├── monitoring_plan.md           ← Four monitoring alerts with response plans
├── images/
│   └── dag_pipeline_architecture.png  ← DAG diagram
├── Week2_Submission_Daniel_Jude.pdf   ← Final PDF submission
├── Week2_Data_Pipeline_Orchestration_LSA.pdf  ← Original brief
└── README.md                    ← This file
```

---

## Skills Demonstrated

- Workflow orchestration using DAG design
- Pipeline dependency management
- Data validation strategies with SQL logic
- Monitoring and alert design
- Connecting Week 1 AWS tools into an automated workflow

---

## Author

**Name:** Daniel Jude<br>
**Programme:** London Success Academy — Data Engineering<br>
**Assignment:** Week 2 — Data Pipeline Orchestration
