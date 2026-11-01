# Power BI semantic model

Import these curated CSVs from `data/processed/` after running `python src/etl.py`:
- `dim_employee.csv`
- `dim_course.csv`
- `fact_enrollment.csv`
- `data_quality_exceptions.csv`

Create relationships (single direction, one-to-many):
- dim_employee[employee_id] 1 -> * fact_enrollment[employee_id]
- dim_course[course_id] 1 -> * fact_enrollment[course_id]

Recommended: create a dedicated Date table, mark it as Date table, and relate Date[Date] 1 -> * fact_enrollment[enrollment_date]. Use a separate inactive relationship to completion_date if needed.

Set data types:
- IDs/text = Text; dates = Date; hours/scores/ratings = Decimal Number; mandatory_flag/active_flag = Whole Number or True/False.
- Format Completion Rate, Mandatory Completion Rate, Learner Participation Rate, Data Quality Pass Rate as Percentage.
- Feedback is 1–5; assessment score is 0–100.

Do not sum employee counts or average pre-aggregated percentages. Use the supplied DAX measures.
