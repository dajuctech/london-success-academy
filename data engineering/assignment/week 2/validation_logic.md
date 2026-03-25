# Data Validation Logic

## Overview

The pipeline performs validation checks on every incoming property dataset before any processing begins. Validation runs first because it is far cheaper to catch bad data at the entry point than to discover errors after it has been transformed, stored, and queried.

If any check fails, the pipeline stops and an alert is sent. Nothing proceeds until the data is confirmed clean.

---

## Important Columns Validated

| Column | Type | Description |
|--------|------|-------------|
| property_id | string | Unique identifier for each property |
| rooms | numeric | Average number of rooms |
| distance | numeric | Distance from employment hubs |
| property_value | numeric | Median property value |

---

## Null Value Check

**What it checks:**
Every row must have a value for all required columns. A record with a missing `property_value`, for example, is useless for price analysis and must be caught before it enters the pipeline.

**SQL logic:**
```sql
SELECT COUNT(*) AS null_count
FROM property_data
WHERE property_id IS NULL
   OR rooms IS NULL
   OR distance IS NULL
   OR property_value IS NULL;
```

**Pass condition:** `null_count = 0`

**What happens if it fails:**
Pipeline stops. Alert sent with the count of null rows and the source filename so the team can identify which agency sent incomplete data.

---

## Duplicate Record Check

**What it checks:**
The same property record should not appear more than once in a daily feed. Duplicates would skew averages and produce misleading reports for real estate clients.

**SQL logic:**
```sql
SELECT property_id, COUNT(*) AS record_count
FROM property_data
GROUP BY property_id
HAVING COUNT(*) > 1;
```

**Pass condition:** Query returns zero rows

**What happens if it fails:**
Pipeline stops. Duplicate rows are logged with counts. The team investigates whether the same file was sent twice or there is a data quality issue at source.

---

## Data Format Validation

**What it checks:**
Values in each column must fall within realistic ranges. A property with zero rooms or a negative value indicates a data entry error or a formatting issue in the source file.

**SQL logic:**
```sql
SELECT COUNT(*) AS invalid_count
FROM property_data
WHERE rooms <= 0
   OR distance < 0
   OR property_value <= 0;
```

**Pass condition:** `invalid_count = 0`

**What happens if it fails:**
Pipeline stops. A sample of the invalid rows is logged so the team can identify the pattern — for example, a source system exporting values in the wrong unit.

---

## Validation Summary

| Check | SQL Logic | Pass Condition | On Failure |
|-------|-----------|----------------|------------|
| Null values | COUNT WHERE any column IS NULL | Count = 0 | Pipeline stops, alert sent |
| Duplicate records | GROUP BY property_id HAVING COUNT > 1 | No rows returned | Pipeline stops, duplicates logged |
| Data format | COUNT WHERE values out of range | Count = 0 | Pipeline stops, sample logged |
