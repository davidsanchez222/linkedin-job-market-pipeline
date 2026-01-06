# Author: David Sanchez
# Email: davidsanchy22@gmail.com
# Purpose: UGAHacks9 LinkedIn Jobs Data Science Project

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import List, Optional, Tuple

SKILL_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("python", re.compile(r"\bpython\b", re.I)),
    ("sql", re.compile(r"\bsql\b", re.I)),
    ("spark", re.compile(r"\bspark\b|\bpyspark\b", re.I)),
    ("hive", re.compile(r"\bhive\b", re.I)),
    ("hadoop", re.compile(r"\bhadoop\b|\bhdfs\b|\bmapreduce\b", re.I)),
    ("kafka", re.compile(r"\bkafka\b", re.I)),
    ("airflow", re.compile(r"\bairflow\b", re.I)),
    ("azkaban", re.compile(r"\bazkaban\b", re.I)),
    ("aws", re.compile(r"\baws\b|\bamazon web services\b", re.I)),
    ("gcp", re.compile(r"\bgcp\b|\bgoogle cloud\b", re.I)),
    ("azure", re.compile(r"\bazure\b", re.I)),
    ("docker", re.compile(r"\bdocker\b", re.I)),
    ("kubernetes", re.compile(r"\bkubernetes\b|\bk8s\b", re.I)),
    ("etl", re.compile(r"\betl\b|\bextract\b.*\btransform\b.*\bload\b", re.I)),
    ("data modeling", re.compile(r"\bdata model(ing)?\b", re.I)),
    ("dbt", re.compile(r"\bdbt\b", re.I)),
    ("snowflake", re.compile(r"\bsnowflake\b", re.I)),
    ("tableau", re.compile(r"\btableau\b", re.I)),
    ("power bi", re.compile(r"\bpower\s*bi\b", re.I)),
    ("scala", re.compile(r"\bscala\b", re.I)),
    ("java", re.compile(r"\bjava\b", re.I)),
]

ROLE_FAMILIES: List[Tuple[str, re.Pattern]] = [
    (
        "data_engineer",
        re.compile(r"\bdata engineer\b|\betl engineer\b|\bdata platform\b", re.I),
    ),
    (
        "data_scientist",
        re.compile(
            r"\bdata scientist\b|\bapplied scientist\b|\bmachine learning scientist\b",
            re.I,
        ),
    ),
    ("ml_engineer", re.compile(r"\bmachine learning engineer\b|\bml engineer\b", re.I)),
    ("analytics", re.compile(r"\banalytics\b|\bbusiness intelligence\b|\bbi\b", re.I)),
    (
        "software_engineer",
        re.compile(r"\bsoftware engineer\b|\bbackend\b|\bfull[- ]stack\b", re.I),
    ),
]


def epoch_ms_to_iso(value) -> Optional[str]:
    """Convert epoch milliseconds (or seconds) to ISO8601 string (UTC)."""
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if v <= 0:
        return None
    if v > 1e11:
        v = v / 1000.0
    dt = datetime.fromtimestamp(v, tz=timezone.utc)
    return dt.isoformat()


def infer_is_remote(title: str, location: str, description: str, remote_allowed) -> int:
    if remote_allowed in (1, True, "1"):
        return 1
    text = " ".join([str(title or ""), str(location or ""), str(description or "")])
    if re.search(r"\bremote\b|\bhybrid\b|\bwork from home\b|\bwfh\b", text, re.I):
        return 1
    return 0


def infer_role_family(title: str) -> str:
    t = (title or "").lower()
    if "data engineer" in t or "etl" in t or "data platform" in t:
        return "data_engineer"
    if "data scientist" in t or "applied scientist" in t:
        return "data_scientist"
    if "machine learning" in t and "engineer" in t:
        return "ml_engineer"
    if "analytics" in t or "business intelligence" in t:
        return "analytics"
    if "software engineer" in t or "backend" in t or "full stack" in t:
        return "software_engineer"
    return "other"


def extract_skills(text: str) -> List[str]:
    if not text:
        return []
    found = []
    for name, pat in SKILL_PATTERNS:
        if pat.search(text):
            found.append(name)
    return sorted(set(found))
