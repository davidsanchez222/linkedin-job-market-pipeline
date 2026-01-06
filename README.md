# LinkedIn Job Pipeline
<img width="1816" height="1012" alt="image" src="https://github.com/user-attachments/assets/ae537c64-56c2-498f-931d-5359907d7421" />


This project implements an end-to-end data engineering pipeline over a LinkedIn-style job postings dataset that I got from Kaggle.

https://www.kaggle.com/datasets/arshkon/linkedin-job-postings/versions/7?resource=download

The pipeline ingests multiple raw data sources produces analytics-ready tables that support skill demand and hiring trend analysis.

The dataset includes both structured fields (job metadata, company information) and unstructured text (job titles and descriptions). This pipeline extracts normalized skill tags from text and consolidates job and company attributes into a single source of truth table for downstream analytics.

This project was originally prototyped during UGAHacks 9 and has since been refactored to focus on production-style ETL design, data modeling, and analytical querying.

---

## Architecture Overview

**Ingest**
- Load multiple raw CSV sources (job postings, company metadata, enrichment tables) into SQLite
- Preserve raw tables for reproducibility and reprocessing

**Transform**
- Normalize job and company attributes into a canonical dimension table (`job_dim`)
- Infer role families (e.g. data engineer, data scientist)
- Infer remote vs onsite roles using structured flags and text
- Extract normalized skill tags from job titles and descriptions
- Produce a skills fact table (`job_skill_facts`)

**Analyze**
- Support analytical queries for skill demand, role distribution, location trends, and remote work patterns
- Example analytical SQL queries are provided in `sql/queries.sql`
- A Streamlit dashboard enables interactive exploration of the results

---

## Data Model

- `job_dim`  
  Canonical job and company dimension table serving as a single source of truth

- `job_skill_facts`  
  Fact table mapping jobs to extracted skill tags

Raw source tables are preserved with a `_raw` suffix for traceability.

---

## Environment Setup (Conda)

```bash
conda env create -f environment.yml
conda activate linkedin-etl
