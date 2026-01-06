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


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--db_path", default="./data/processed/jobs.db", help="SQLite database path"
    )
    p.add_argument(
        "--out_dir", default="./data/processed", help="Where to write CSV outputs"
    )
    args = p.parse_args()

    conn = sqlite3.connect(args.db_path)

    top_skills = pd.read_sql_query(
        """
        SELECT skill, COUNT(*) AS job_count
        FROM job_skill_facts
        GROUP BY skill
        ORDER BY job_count DESC
        LIMIT 25;
    """,
        conn,
    )

    de_skills = pd.read_sql_query(
        """
        SELECT s.skill, COUNT(*) AS job_count
        FROM job_skill_facts s
        JOIN job_dim d USING(job_id)
        WHERE d.role_family='data_engineer'
        GROUP BY s.skill
        ORDER BY job_count DESC
        LIMIT 25;
    """,
        conn,
    )

    out_dir = args.out_dir
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    top_skills.to_csv(f"{out_dir}/top_skills.csv", index=False)
    de_skills.to_csv(f"{out_dir}/data_engineer_top_skills.csv", index=False)

    conn.close()
    print("Wrote CSV analytics outputs to:", out_dir)


if __name__ == "__main__":
    main()
