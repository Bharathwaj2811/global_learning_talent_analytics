# KPI dictionary

| KPI | Definition | Grain / caveat |
|---|---|---|
| Enrollments | Count of curated enrollment IDs | Enrollment grain |
| Completed enrollments | Count where status = Completed | Enrollment grain |
| Completion rate | Completed enrollments / all curated enrollments | Filter-sensitive; not unique learner completion |
| Unique learners | Distinct employee IDs with an enrollment | Selected period/filter context |
| Learner participation rate | Unique learners / active employee population | Population denominator should be agreed with HR |
| Learning hours | Sum of completed_hours | Includes partial progress where recorded |
| Average feedback | Mean feedback_rating for completed records | Only respondents with a rating |
| Assessment score | Mean assessment_score for completed records | Only assessed completions |
| Mandatory completion rate | Completed mandatory enrollments / mandatory enrollments | Course mandatory flag |
| Overdue open enrollments | Mandatory, non-completed records with due_date before today | Time-dependent; refresh date matters |
| Data quality exceptions | Count of exception log rows | One record may have multiple exceptions |
| Data quality pass rate | 1 - exception count / raw row count | Can be below zero if multiple exceptions per row; use unique affected rows for formal SLA |

**Governance note:** Agree definitions, population scope, exclusions, refresh cutoff, and owner with stakeholders before operational use.
