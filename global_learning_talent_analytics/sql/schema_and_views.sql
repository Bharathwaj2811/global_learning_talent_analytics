PRAGMA foreign_keys = ON;
DROP VIEW IF EXISTS vw_learning_monthly;
DROP VIEW IF EXISTS vw_department_learning;
DROP VIEW IF EXISTS vw_data_quality_exceptions;
DROP TABLE IF EXISTS data_quality_exceptions;
DROP TABLE IF EXISTS fact_enrollment;
DROP TABLE IF EXISTS dim_course;
DROP TABLE IF EXISTS dim_employee;

CREATE TABLE dim_employee (
 employee_id TEXT PRIMARY KEY, department TEXT NOT NULL, region TEXT NOT NULL,
 country_city TEXT, job_level TEXT, hire_date DATE, employment_status TEXT
);
CREATE TABLE dim_course (
 course_id TEXT PRIMARY KEY, course_name TEXT NOT NULL, learning_category TEXT,
 duration_hours REAL, mandatory_flag INTEGER, course_owner TEXT, delivery_mode TEXT, active_flag INTEGER
);
CREATE TABLE data_quality_exceptions (
 enrollment_id TEXT, exception_type TEXT, field TEXT, observed_value TEXT
);
CREATE TABLE fact_enrollment (
 enrollment_id TEXT PRIMARY KEY, employee_id TEXT, course_id TEXT,
 enrollment_date DATE, due_date DATE, completion_date DATE, status TEXT,
 completed_hours REAL, assessment_score REAL, feedback_rating REAL, source_system TEXT,
 FOREIGN KEY(employee_id) REFERENCES dim_employee(employee_id),
 FOREIGN KEY(course_id) REFERENCES dim_course(course_id)
);
CREATE INDEX idx_enrollment_date ON fact_enrollment(enrollment_date);
CREATE INDEX idx_enrollment_status ON fact_enrollment(status);
CREATE INDEX idx_enrollment_employee ON fact_enrollment(employee_id);

CREATE VIEW vw_learning_monthly AS
SELECT strftime('%Y-%m', f.enrollment_date) AS reporting_month,
       COUNT(*) AS enrollments,
       SUM(CASE WHEN f.status='Completed' THEN 1 ELSE 0 END) AS completions,
       ROUND(100.0*SUM(CASE WHEN f.status='Completed' THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate_pct,
       ROUND(SUM(f.completed_hours),2) AS learning_hours,
       ROUND(AVG(CASE WHEN f.status='Completed' THEN f.feedback_rating END),2) AS avg_feedback
FROM fact_enrollment f
GROUP BY strftime('%Y-%m', f.enrollment_date);

CREATE VIEW vw_department_learning AS
SELECT e.department, e.region, COUNT(*) AS enrollments,
       SUM(CASE WHEN f.status='Completed' THEN 1 ELSE 0 END) AS completions,
       ROUND(100.0*SUM(CASE WHEN f.status='Completed' THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate_pct,
       ROUND(AVG(CASE WHEN f.status='Completed' THEN f.feedback_rating END),2) AS avg_feedback,
       ROUND(SUM(f.completed_hours),2) AS learning_hours
FROM fact_enrollment f JOIN dim_employee e ON f.employee_id=e.employee_id
GROUP BY e.department,e.region;

CREATE VIEW vw_data_quality_exceptions AS
SELECT enrollment_id, exception_type, observed_value AS exception_value
FROM data_quality_exceptions;
