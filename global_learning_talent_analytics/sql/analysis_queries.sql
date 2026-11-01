-- 1. Monthly learning trend
SELECT * FROM vw_learning_monthly ORDER BY reporting_month;

-- 2. Department and region scorecard
SELECT * FROM vw_department_learning ORDER BY department, region;

-- 3. Mandatory learning overdue (as-of date supplied by analyst)
SELECT e.department, e.region, COUNT(*) AS overdue_open_enrollments
FROM fact_enrollment f JOIN dim_employee e USING(employee_id)
JOIN dim_course c USING(course_id)
WHERE c.mandatory_flag=1 AND f.status<>'Completed'
  AND date(f.due_date) < date('now')
GROUP BY e.department,e.region
ORDER BY overdue_open_enrollments DESC;

-- 4. Course effectiveness
SELECT c.course_name, COUNT(*) AS enrollments,
       ROUND(AVG(f.assessment_score),1) AS avg_assessment_score,
       ROUND(AVG(f.feedback_rating),2) AS avg_feedback
FROM fact_enrollment f JOIN dim_course c USING(course_id)
WHERE f.status='Completed'
GROUP BY c.course_name ORDER BY enrollments DESC;

-- 5. Data quality exception counts
SELECT exception_type, COUNT(*) AS exception_count
FROM vw_data_quality_exceptions GROUP BY exception_type ORDER BY exception_count DESC;
