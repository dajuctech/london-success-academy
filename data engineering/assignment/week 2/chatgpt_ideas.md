Good question. I’ll walk you through **exactly how to do the Week 2 assignment from beginning → submission** in a **very beginner-friendly way**, especially since you are using **VS Code and GitHub**.

Your assignment file explains that your job is to **design a DAG workflow to automate a data pipeline** for property data that arrives daily in **Amazon S3**. 

---

# 1. First understand what Week 2 is asking

The company now receives **daily property data updates**, so running the pipeline manually is not efficient. Your job is to **design a workflow that runs automatically using a DAG**. 

The pipeline should automatically do these steps:

1. Validate data
2. Clean data
3. Transform dataset
4. Store processed data
5. Update analytics tables

These steps will become the **DAG nodes**. 

---

# 2. What you actually need to submit

Your assignment requires **4 things**:

1. DAG architecture diagram
2. Pipeline workflow documentation
3. Validation logic explanation
4. Monitoring strategy

These are the **deliverables** listed in the assignment. 

You are **not required to build a real Airflow pipeline yet**.
You just need to **design and explain the workflow**.

---

# 3. Create your Week 2 folder in VS Code

Inside your GitHub repository:

```
london-success-academy
```

Create a new folder:

```
data-engineering/assignment/week2
```

Inside it create this structure:

```
week2/
│
├── README.md
├── dag_architecture.md
├── pipeline_workflow.md
├── validation_logic.md
├── monitoring_plan.md
└── images/
```

---

# 4. Step 1 — Create the DAG architecture diagram

Your pipeline flow should look like this:

```
Data Upload (S3)
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

You can create this diagram using:

**Option 1 (easiest)**
draw.io

[https://draw.io](https://draw.io)

**Option 2**

Lucidchart

**Option 3**

PowerPoint

---

### Save the diagram

Save the image as:

```
dag_pipeline_architecture.png
```

Place it inside:

```
images/
```

---

# 5. Step 2 — Write the pipeline workflow documentation

Create file:

```
pipeline_workflow.md
```

Example content:

```
# Pipeline Workflow Documentation

This pipeline automates the daily processing of property data received from multiple real estate agencies.

The workflow is controlled using a Directed Acyclic Graph (DAG).

## Pipeline Steps

1. Data Upload
Property datasets arrive daily in an Amazon S3 bucket.

2. Data Validation
The pipeline validates incoming datasets to ensure data quality.

3. Data Cleaning
Invalid records, duplicates, and missing values are removed.

4. Data Transformation
The dataset is transformed into a structured format suitable for analytics.

5. Data Storage
The processed dataset is stored in Parquet format in the processed data layer.

6. Analytics Trigger
The pipeline triggers analytics queries to refresh reporting tables.
```

---

# 6. Step 3 — Write the validation logic

Create file:

```
validation_logic.md
```

Example content:

```
# Data Validation Logic

The pipeline performs several checks to ensure the quality of incoming property datasets.

## Null Value Check

The system checks whether critical columns contain missing values.

Examples of important columns:

- property_id
- rooms
- distance
- property_value

Rows with missing values are flagged or removed.

## Duplicate Record Check

The pipeline checks if the same property record appears multiple times.

Duplicate records are removed during the cleaning phase.

## Data Format Validation

The system validates data types:

rooms → numeric
distance → numeric
property_value → numeric

Invalid formats are flagged during validation.
```

---

# 7. Step 4 — Create the monitoring strategy

Create file:

```
monitoring_plan.md
```

Example content:

```
# Monitoring Strategy

Monitoring ensures that the pipeline runs reliably and errors are detected quickly.

## Pipeline Failure Alert

If any task in the DAG fails, an alert should be triggered to notify the data engineering team.

## Missing Data Alert

If no daily dataset arrives in the S3 bucket, the system should generate an alert.

## Job Execution Error

If an ETL job crashes or times out, the pipeline should log the error and notify engineers.

## Data Quality Alert

If validation detects a high number of invalid records, a warning alert should be generated.
```

---

# 8. Step 5 — Write the main README

Create:

```
README.md
```

Example:

```
# Week 2 Assignment – Data Pipeline Orchestration

London Success Academy Joint Internship Programme  
Data-SPARK Mentorship – Venkat Potamsetti

## Project Scenario

MarketFlow Property Intelligence receives daily property data updates from multiple real estate agencies. Running data pipelines manually is inefficient, so the company needs an automated workflow.

This assignment focuses on designing a Directed Acyclic Graph (DAG) to automate the data processing pipeline.

## DAG Workflow

The pipeline performs the following tasks:

1. Validate incoming data
2. Clean the dataset
3. Transform the dataset
4. Store processed data
5. Trigger analytics queries

## Pipeline Architecture

![DAG Architecture](images/dag_pipeline_architecture.png)

## Files in this Project

dag_architecture.md – DAG design explanation  
pipeline_workflow.md – pipeline workflow documentation  
validation_logic.md – validation rules explanation  
monitoring_plan.md – monitoring strategy

## Skills Demonstrated

- Workflow orchestration
- DAG architecture design
- Pipeline dependency management
- Data validation strategies
- Monitoring and alert design
```

---

# 9. Convert everything to PDF for submission

Because your assignment says **submit as PDF**.

### Method 1 (easiest)

Use VS Code:

Install extension:

```
Markdown PDF
```

Then:

```
Right click README.md
Export → PDF
```

---

### Method 2

Upload markdown files to:

```
https://stackedit.io
```

Export as PDF.

---

# 10. Push to GitHub

In VS Code terminal:

```
git add .
git commit -m "Week 2 Data Pipeline Orchestration Assignment"
git push
```

Your repo will look like:

```
week2
│
├── README.md
├── dag_architecture.md
├── pipeline_workflow.md
├── validation_logic.md
├── monitoring_plan.md
└── images
      └── dag_pipeline_architecture.png
```

---

# 11. The key thing your mentor wants to see

You must demonstrate understanding of:

* **DAG workflow**
* **Pipeline dependencies**
* **Data validation**
* **Monitoring**

Those are the **Week 2 learning objectives** in the assignment. 

---

# 12. What Week 3 will likely introduce

Week 2 is **design only**.

Week 3 will probably introduce:

* **Apache Airflow**
* **real DAG code**
* **pipeline scheduling**

---

✅ If you want, I can also give you:

* **a ready-made DAG diagram you can submit**
* **the exact Week 2 PDF report format your mentor expects (Distinction level)**
* **a simple Airflow DAG example (optional but impressive for your submission)**.

The **first step for Week 2** is **not coding yet**.
The first thing you need to do is **understand and design the pipeline workflow** before writing anything.

Your assignment clearly says the goal is to **design a DAG to automate the data pipeline workflow**. 

So the **very first thing to do** is to **understand the pipeline steps and draw the workflow**.

---

# Step 1 — Understand the pipeline scenario

Read the assignment and identify the **main pipeline steps**.

The company receives **daily property data in Amazon S3**, and the system must automatically perform these tasks:

1. Validate data
2. Clean data
3. Transform dataset
4. Store processed dataset
5. Update analytics tables 

So your workflow becomes:

```
S3 Data Upload
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

This flow is your **DAG design**.

---

# Step 2 — Create your Week 2 project folder

Open **VS Code** and create the assignment folder.

Inside your GitHub repository:

```
london-success-academy
   ↓
data engineering
   ↓
assignment
   ↓
week 2
```

Create this structure:

```
week2
│
├── README.md
├── pipeline_workflow.md
├── validation_logic.md
├── monitoring_plan.md
└── images
```

Do this **before writing anything**.

---

# Step 3 — Draw the DAG architecture diagram

This is the **first deliverable your mentor expects**.

Use a tool like:

* draw.io (recommended)
* Lucidchart
* PowerPoint

Create a simple diagram like this:

```
Daily Property Data (S3)
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

Export it as:

```
dag_pipeline_architecture.png
```

Save it inside:

```
week2/images/
```

---

# Step 4 — Write the pipeline explanation

Next create this file:

```
pipeline_workflow.md
```

Explain what each task does.

Example:

### task_1_validate_data

Check incoming datasets for errors such as missing values, duplicate records, or invalid formats.

### task_2_clean_data

Remove duplicates and incomplete records.

### task_3_transform_dataset

Convert the cleaned dataset into a structured format suitable for analytics.

### task_4_store_parquet

Store the processed dataset in Parquet format in the processed data layer.

### task_5_trigger_analytics

Update analytics queries or reporting dashboards.

---

# Step 5 — Write the validation logic

Create:

```
validation_logic.md
```

Explain:

* Null value checks
* Duplicate detection
* Data format validation

These checks are specifically required in the assignment. 

---

# Step 6 — Write the monitoring plan

Create:

```
monitoring_plan.md
```

Explain how the pipeline detects problems:

Examples:

* pipeline failure alerts
* missing data alerts
* ETL job errors

Monitoring strategy is also required in the assignment. 

---

# Step 7 — Write the README summary

Create:

```
README.md
```

Explain:

* the scenario
* the pipeline architecture
* the DAG workflow
* the validation logic
* the monitoring plan

---

# Step 8 — Export the assignment as PDF

Since your mentor asked for **PDF submission**, you can export your README or combine the markdown files into a PDF.

VS Code extension:

```
Markdown PDF
```

Then export.

---

# The **very first 3 things you should do now**

1️⃣ Create the **week2 folder in VS Code**
2️⃣ Draw the **DAG architecture diagram**
3️⃣ Save the diagram inside **images folder**

Only after that should you start writing the documentation.

---

If you want, I can also show you the **exact DAG diagram that most students submit for Week 2** (so you can copy it and finish the assignment in **30 minutes**).

Yes — **exactly. Week 2 builds on the work you did in Week 1.** 👍
You are **not starting a new project**. You are **adding automation and orchestration to the pipeline you already built.**

In **Week 1**, you built the pipeline manually:

```
CSV → S3 → Glue → Athena
```

You uploaded data, ran Glue crawler, created tables, and queried the data.

---

# What Week 2 is doing

Week 2 asks:

> How can this pipeline run automatically every day without manual work?

So instead of manually doing the steps, you **design a workflow (DAG)** that controls the order of tasks.

Your assignment says the company now receives **daily property data updates**, so the pipeline must be automated. 

---

# What your Week 2 pipeline should look like

Now combine Week 1 with automation logic.

```
New CSV arrives in S3
        ↓
Validate dataset
        ↓
Clean dataset
        ↓
Transform dataset (Glue ETL)
        ↓
Store processed dataset (Parquet in S3)
        ↓
Update Athena tables
```

This is your **DAG workflow**.

---

# What you should do now (Step-by-Step)

## Step 1 — Go to your Week 2 folder in VS Code

Inside your repo:

```
london-success-academy
   ↓
data engineering
   ↓
assignment
   ↓
week2
```

Create this structure:

```
week2
│
├── README.md
├── pipeline_workflow.md
├── validation_logic.md
├── monitoring_plan.md
└── images
```

---

# Step 2 — Draw the pipeline diagram (FIRST THING)

Since you already built Week 1, your diagram should include those tools.

Example architecture:

```
Property CSV
     ↓
Amazon S3 (raw data)
     ↓
Data Validation
     ↓
Data Cleaning
     ↓
AWS Glue ETL
     ↓
S3 Processed Layer (Parquet)
     ↓
AWS Athena
     ↓
Analytics Query
```

Save the diagram as:

```
dag_pipeline_architecture.png
```

Put it in:

```
week2/images/
```

---

# Step 3 — Explain the workflow

Create:

```
pipeline_workflow.md
```

Explain the pipeline like this:

### Data Upload

Daily property datasets arrive in Amazon S3.

### Data Validation

The pipeline checks for missing values, duplicates, and incorrect data formats.

### Data Cleaning

Invalid records are removed.

### Data Transformation

AWS Glue transforms the dataset and converts it into Parquet format.

### Data Storage

The processed dataset is stored in the processed layer in S3.

### Analytics Query

AWS Athena queries the processed dataset for analytics.

---

# Step 4 — Write validation logic

Create:

```
validation_logic.md
```

Explain checks such as:

### Null Value Check

Ensure important columns like:

* rooms
* distance
* property_value

do not contain missing values.

### Duplicate Record Check

Remove duplicate rows.

### Format Validation

Ensure numeric columns contain valid numbers.

---

# Step 5 — Create monitoring plan

Create:

```
monitoring_plan.md
```

Explain how the pipeline detects issues.

Example:

### Pipeline Failure Alert

Alert the engineering team if any pipeline step fails.

### Missing Data Alert

Alert if no daily file arrives in S3.

### Job Execution Error

Detect failures during ETL transformation.

---

# Step 6 — Write the README

Create:

```
README.md
```

This should contain:

* project overview
* DAG workflow
* pipeline architecture
* validation logic
* monitoring plan

---

# What your mentor expects for Week 2

Your submission should contain:

1️⃣ **DAG architecture diagram**
2️⃣ **Pipeline workflow documentation**
3️⃣ **Validation logic explanation**
4️⃣ **Monitoring strategy**

Those are the **official deliverables**. 

---

# Very important (how Week 1 connects to Week 2)

Week 1 tools should appear in your diagram:

| Week 1 Tool | Week 2 Role        |
| ----------- | ------------------ |
| S3          | Raw data storage   |
| Glue        | ETL transformation |
| Athena      | Analytics query    |
| Parquet     | Processed dataset  |

So your architecture diagram should look **professional**.

---

# What I recommend you do right now

**Do these 3 things first:**

1️⃣ Open **draw.io**
2️⃣ Draw the pipeline architecture
3️⃣ Save it as:

```
dag_pipeline_architecture.png
```

---

If you want, I can also show you:

**The exact DAG architecture diagram most London Success Academy students submit**
(it will make your Week 2 assignment **10x easier and look professional**).
