"""Build a validated SQLite reporting mart from raw CSV inputs."""
from pathlib import Path
import sqlite3, pandas as pd, json
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data"/"raw"
PROC=ROOT/"data"/"processed"
DB=ROOT/"data"/"learning_analytics.db"

def main():
    PROC.mkdir(exist_ok=True)
    employees=pd.read_csv(RAW/"employees.csv")
    courses=pd.read_csv(RAW/"courses.csv")
    enrollments=pd.read_csv(RAW/"enrollments.csv")
    exceptions=[]
    def record(mask, code, col):
        for _,r in enrollments.loc[mask].iterrows():
            exceptions.append({"enrollment_id":r["enrollment_id"],"exception_type":code,"field":col,"observed_value":str(r[col])})
    record(~enrollments.employee_id.isin(employees.employee_id),"UNKNOWN_EMPLOYEE","employee_id")
    record(~enrollments.course_id.isin(courses.course_id),"UNKNOWN_COURSE","course_id")
    record(enrollments.completed_hours.lt(0),"NEGATIVE_COMPLETED_HOURS","completed_hours")
    record(enrollments.feedback_rating.notna() & ~enrollments.feedback_rating.between(1,5),"FEEDBACK_OUT_OF_RANGE","feedback_rating")
    record(enrollments.assessment_score.notna() & ~enrollments.assessment_score.between(0,100),"ASSESSMENT_OUT_OF_RANGE","assessment_score")
    record(enrollments.enrollment_id.duplicated(keep=False),"DUPLICATE_ENROLLMENT_ID","enrollment_id")
    # Preserve raw records, but quarantine invalid facts from curated mart.
    valid=(enrollments.employee_id.isin(employees.employee_id)
           & enrollments.course_id.isin(courses.course_id)
           & enrollments.completed_hours.ge(0)
           & (enrollments.feedback_rating.isna() | enrollments.feedback_rating.between(1,5))
           & (enrollments.assessment_score.isna() | enrollments.assessment_score.between(0,100))
           & ~enrollments.enrollment_id.duplicated(keep=False))
    curated=enrollments.loc[valid].copy()
    exceptions_df=pd.DataFrame(exceptions,columns=["enrollment_id","exception_type","field","observed_value"])
    employees.to_csv(PROC/"dim_employee.csv",index=False)
    courses.to_csv(PROC/"dim_course.csv",index=False)
    curated.to_csv(PROC/"fact_enrollment.csv",index=False)
    exceptions_df.to_csv(PROC/"data_quality_exceptions.csv",index=False)
    with sqlite3.connect(DB) as con:
        con.executescript((ROOT/"sql"/"schema_and_views.sql").read_text())
        employees.to_sql("dim_employee",con,if_exists="append",index=False)
        courses.to_sql("dim_course",con,if_exists="append",index=False)
        curated.to_sql("fact_enrollment",con,if_exists="append",index=False)
        exceptions_df.to_sql("data_quality_exceptions",con,if_exists="append",index=False)
        # Views created by schema script
        checks={
          "raw_enrollments":int(len(enrollments)),
          "curated_enrollments":int(len(curated)),
          "quarantined_enrollments":int(len(enrollments)-len(curated)),
          "exceptions":int(len(exceptions_df)),
          "duplicate_enrollment_ids":int(enrollments.enrollment_id.duplicated().sum())
        }
    (PROC/"etl_quality_summary.json").write_text(json.dumps(checks,indent=2))
    print(json.dumps(checks,indent=2))
if __name__=="__main__": main()
