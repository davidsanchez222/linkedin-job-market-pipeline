import os
import sqlite3

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Job Market Skill Analytics", layout="wide")
DB_PATH = os.getenv("DB_PATH", "./data/processed/jobs.db")


@st.cache_data(ttl=300)
def load_table(query: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


st.title("Job Market Skill Analytics")
st.caption(
    "ETL pipeline producing a single source of truth (job_dim) and skill facts (job_skill_facts)."
)

col1, col2, col3 = st.columns(3)
with col1:
    role = st.selectbox(
        "Role family",
        [
            "all",
            "data_engineer",
            "data_scientist",
            "ml_engineer",
            "analytics",
            "software_engineer",
            "other",
        ],
    )
with col2:
    remote_only = st.selectbox("Work mode", ["all", "remote", "onsite"])
with col3:
    top_n = st.slider("Top N skills", 5, 30, 15)

where = []
if role != "all":
    where.append(f"d.role_family = '{role}'")
if remote_only == "remote":
    where.append("d.is_remote = 1")
elif remote_only == "onsite":
    where.append("d.is_remote = 0")
where_sql = ("WHERE " + " AND ".join(where)) if where else ""

top_skills = load_table(
    f"""
SELECT s.skill, COUNT(*) AS job_count
FROM job_skill_facts s
JOIN job_dim d USING(job_id)
{where_sql}
GROUP BY s.skill
ORDER BY job_count DESC
LIMIT {top_n};
"""
)

st.subheader("Top Skills")
st.dataframe(top_skills, use_container_width=True)

st.subheader("Recent Jobs (sample)")
sample_jobs = load_table(
    f"""
SELECT d.posted_at, d.title, d.company_name, d.location, d.is_remote, d.role_family, d.job_posting_url
FROM job_dim d
{where_sql}
ORDER BY d.posted_at DESC
LIMIT 25;
"""
)
st.dataframe(sample_jobs, use_container_width=True)
