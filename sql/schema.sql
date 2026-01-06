PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS job_postings_raw (
  job_id INTEGER PRIMARY KEY,
  company_id INTEGER,
  title TEXT,
  description TEXT,
  max_salary REAL,
  med_salary REAL,
  min_salary REAL,
  pay_period TEXT,
  formatted_work_type TEXT,
  location TEXT,
  applies INTEGER,
  original_listed_time REAL,
  remote_allowed REAL,
  views INTEGER,
  job_posting_url TEXT,
  application_url TEXT,
  application_type TEXT,
  expiry REAL,
  closed_time REAL,
  formatted_experience_level TEXT,
  skills_desc TEXT,
  listed_time REAL,
  posting_domain TEXT,
  sponsored REAL,
  work_type TEXT,
  currency TEXT,
  compensation_type TEXT
);

CREATE TABLE IF NOT EXISTS companies_raw (
  company_id INTEGER PRIMARY KEY,
  name TEXT,
  description TEXT,
  company_size TEXT,
  state TEXT,
  country TEXT,
  city TEXT,
  zip_code TEXT,
  address TEXT,
  url TEXT
);

CREATE TABLE IF NOT EXISTS employee_counts_raw (
  company_id INTEGER,
  employee_count INTEGER,
  follower_count INTEGER,
  time_recorded REAL
);

CREATE TABLE IF NOT EXISTS job_industries_raw (
  job_id INTEGER,
  industry_id INTEGER
);

CREATE TABLE IF NOT EXISTS benefits_raw (
  job_id INTEGER,
  inferred INTEGER,
  type TEXT
);

CREATE TABLE IF NOT EXISTS company_industries_raw (
  company_id INTEGER,
  industry TEXT
);

CREATE TABLE IF NOT EXISTS company_specialities_raw (
  company_id INTEGER,
  speciality TEXT
);

CREATE TABLE IF NOT EXISTS job_skills_raw (
  job_id INTEGER,
  skill_abr TEXT
);

CREATE TABLE IF NOT EXISTS job_dim (
  job_id INTEGER PRIMARY KEY,
  company_id INTEGER,
  company_name TEXT,
  company_size TEXT,
  employee_count INTEGER,
  follower_count INTEGER,
  title TEXT,
  role_family TEXT,
  formatted_work_type TEXT,
  location TEXT,
  is_remote INTEGER,
  experience_level TEXT,
  posted_at TEXT, -- ISO timestamp
  job_posting_url TEXT
);

CREATE TABLE IF NOT EXISTS job_skill_facts (
  job_id INTEGER,
  skill TEXT,
  PRIMARY KEY (job_id, skill)
);

CREATE INDEX IF NOT EXISTS idx_job_dim_role_family ON job_dim(role_family);
CREATE INDEX IF NOT EXISTS idx_job_dim_location ON job_dim(location);
CREATE INDEX IF NOT EXISTS idx_job_skill_skill ON job_skill_facts(skill);

