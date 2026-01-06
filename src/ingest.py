# Author: David Sanchez
# Email: davidsanchy22@gmail.com
# Purpose: UGAHacks9 LinkedIn Jobs Data Science Project

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

import argparse
import sqlite3

import pandas as pd

RAW_FILES = {
    "job_postings_raw": "job_postings.csv",
    "job_skills_raw": "job_details/job_skills.csv",
    "job_industries_raw": "job_details/job_industries.csv",
    "benefits_raw": "job_details/benefits.csv",
    "companies_raw": "company_details/companies.csv",
    "employee_counts_raw": "company_details/employee_counts.csv",
    "company_industries_raw": "company_details/company_industries.csv",
    "company_specialities_raw": "company_details/company_specialities.csv",
}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data_dir", default="./data/raw")
    p.add_argument("--db_path", default="./data/processed/jobs.db")
    p.add_argument("--schema", default="./sql/schema.sql")
    args = p.parse_args()

    data_dir = Path(args.data_dir)
    db_path = Path(args.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.executescript(Path(args.schema).read_text(encoding="utf-8"))

    for table, rel_path in RAW_FILES.items():
        csv_path = data_dir / rel_path
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing expected file: {csv_path}")

        print(f"Loading {csv_path} -> {table}")
        df = pd.read_csv(csv_path)

        if "job_id" in df.columns:
            df["job_id"] = pd.to_numeric(df["job_id"], errors="coerce")
        if "company_id" in df.columns:
            df["company_id"] = pd.to_numeric(df["company_id"], errors="coerce")

        df.to_sql(table, conn, if_exists="replace", index=False)

    conn.close()
    print(f"Done. SQLite DB at: {db_path}")


if __name__ == "__main__":
    main()
