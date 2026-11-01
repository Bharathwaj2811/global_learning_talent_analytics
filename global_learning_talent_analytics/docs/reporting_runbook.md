# Reporting runbook

1. Obtain approved source extracts and confirm reporting cutoff.
2. Place files in `data/raw/` using the expected filenames and column schema.
3. Run `python src/etl.py`.
4. Review `data/processed/etl_quality_summary.json` and exception CSV.
5. Investigate material exceptions; do not distribute unvalidated results.
6. Run SQL queries in `sql/analysis_queries.sql` and reconcile headline metrics.
7. Refresh Power BI model; verify filter context and totals.
8. Export approved visuals to PowerPoint and add reporting period, refresh timestamp, definitions and caveats.
9. Save a versioned copy and archive the exception summary.
10. Escalate methodology, population, or data ownership questions to the reporting lead.
