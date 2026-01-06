-- example queries to run for people running this project locally

-- Top skills overall
SELECT skill, COUNT(*) AS job_count
FROM job_skill_facts
GROUP BY skill
ORDER BY job_count DESC
LIMIT 20;

-- Top skills for data engineer roles
SELECT s.skill, COUNT(*) AS job_count
FROM job_skill_facts s
JOIN job_dim d USING(job_id)
WHERE d.role_family = 'data_engineer'
GROUP BY s.skill
ORDER BY job_count DESC
LIMIT 20;

-- Remote vs onsite skill demand
SELECT d.is_remote, s.skill, COUNT(*) AS job_count
FROM job_skill_facts s
JOIN job_dim d USING(job_id)
GROUP BY d.is_remote, s.skill
ORDER BY job_count DESC;

-- Top locations by posting volume
SELECT location, COUNT(*) AS postings
FROM job_dim
GROUP BY location
ORDER BY postings DESC
LIMIT 10;

