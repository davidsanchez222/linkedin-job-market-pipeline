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

from utils import epoch_ms_to_iso, extract_skills, infer_is_remote, infer_role_family


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--db_path", default="./data/processed/jobs.db", help="SQLite database path"
    )
    args = p.parse_args()

    db_path = Path(args.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Opening DB: {db_path}")
    conn = sqlite3.connect(str(db_path))

    jobs = pd.read_sql_query(
        """
        SELECT job_id, company_id, title, description, skills_desc, remote_allowed, location,
               listed_time, formatted_experience_level, formatted_work_type, job_posting_url
        FROM job_postings_raw;
        """,
        conn,
    )
    companies = pd.read_sql_query(
        "SELECT company_id, name, company_size FROM companies_raw;",
        conn,
    )
    emp = pd.read_sql_query(
        "SELECT company_id, employee_count, follower_count, time_recorded FROM employee_counts_raw;",
        conn,
    )

    print(
        f"Loaded jobs={len(jobs):,} companies={len(companies):,} employee_counts={len(emp):,}"
    )

    if not emp.empty:
        emp = emp.sort_values(["company_id", "time_recorded"]).drop_duplicates(
            "company_id", keep="last"
        )
        emp = emp[["company_id", "employee_count", "follower_count"]]
    else:
        emp = pd.DataFrame(columns=["company_id", "employee_count", "follower_count"])

    df = jobs.merge(companies, on="company_id", how="left")
    df = df.merge(emp, on="company_id", how="left")

    df["company_name"] = df["name"]
    df["role_family"] = df["title"].apply(infer_role_family)

    df["is_remote"] = df.apply(
        lambda r: infer_is_remote(
            r.get("title"),
            r.get("location"),
            r.get("description"),
            r.get("remote_allowed"),
        ),
        axis=1,
    )

    df["posted_at"] = df["listed_time"].apply(epoch_ms_to_iso)
    df["experience_level"] = df["formatted_experience_level"]

    job_dim = df[
        [
            "job_id",
            "company_id",
            "company_name",
            "company_size",
            "employee_count",
            "follower_count",
            "title",
            "role_family",
            "formatted_work_type",
            "location",
            "is_remote",
            "experience_level",
            "posted_at",
            "job_posting_url",
        ]
    ].copy()

    print("Extracting skills from text fields (title + skills_desc + description)...")
    text_series = (
        df["title"].fillna("").astype(str)
        + " "
        + df["skills_desc"].fillna("").astype(str)
        + " "
        + df["description"].fillna("").astype(str)
    )

    skills_list = text_series.apply(extract_skills)
    facts = pd.DataFrame({"job_id": df["job_id"].astype(int), "skills": skills_list})
    facts = facts.explode("skills").dropna()
    facts = facts.rename(columns={"skills": "skill"})
    facts["skill"] = facts["skill"].astype(str)
    facts = facts.drop_duplicates(subset=["job_id", "skill"])

    print(f"Built job_dim rows: {len(job_dim):,}")
    print(f"Built job_skill_facts rows: {len(facts):,}")

    conn.execute("DELETE FROM job_dim;")
    conn.execute("DELETE FROM job_skill_facts;")
    conn.commit()

    job_dim.to_sql("job_dim", conn, if_exists="append", index=False)
    facts.to_sql("job_skill_facts", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()
