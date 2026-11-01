# Power BI dashboard design specification

## Global layout
16:9 canvas; white background; navy headers; teal highlights; restrained red/amber/green status colors. Keep a consistent reporting period and refresh timestamp in the header. Use accessible labels and avoid relying on color alone.

## Page 1 — Executive Overview
Top KPI cards: Total Enrollments, Completion Rate, Total Learning Hours, Average Feedback, Overdue Mandatory Enrollments.
Visuals: monthly enrollment/completion combo chart; completion rate by department; status distribution; region slicer, department slicer, date slicer.
Insight callout: highest completion gap and department/region needing follow-up.

## Page 2 — Participation & Completion
Visuals: monthly trend, department x region matrix with enrollment/completion rate, status stacked bar, job level breakdown.
Slicers: reporting month, region, department, job level, delivery mode.
Drill-through: department detail.

## Page 3 — Course Effectiveness
Visuals: course ranking by enrollment, average assessment score, feedback rating, delivery mode comparison.
Tooltip: course category, mandatory flag, duration, owner.
Caution: feedback is respondent-based and may be biased by response rate.

## Page 4 — Data Quality & Controls
Cards: raw row count, curated row count, quarantined rows, exceptions.
Visuals: exceptions by type, exception trend if timestamped snapshots are added, exception detail table with enrollment ID, field, observed value.
Include data refresh date, data owner, validation status and sign-off.

## Reconciliation checklist
Before publishing, reconcile Power BI totals to SQL for the same filters and date cutoff. Confirm excluded rows, duplicate handling, and denominator definitions. Record reviewer and refresh timestamp.
