import unittest, sqlite3, subprocess, sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
class TestLearningAnalytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable,str(ROOT/"src"/"etl.py")],check=True,cwd=ROOT,capture_output=True,text=True)
        cls.db=ROOT/"data"/"learning_analytics.db"
    def test_curated_facts_have_valid_employee_and_course(self):
        with sqlite3.connect(self.db) as c:
            bad=c.execute("""SELECT COUNT(*) FROM fact_enrollment f
              LEFT JOIN dim_employee e USING(employee_id)
              LEFT JOIN dim_course d USING(course_id)
              WHERE e.employee_id IS NULL OR d.course_id IS NULL""").fetchone()[0]
        self.assertEqual(bad,0)
    def test_no_negative_hours(self):
        with sqlite3.connect(self.db) as c:
            n=c.execute("SELECT COUNT(*) FROM fact_enrollment WHERE completed_hours<0").fetchone()[0]
        self.assertEqual(n,0)
    def test_feedback_range(self):
        with sqlite3.connect(self.db) as c:
            n=c.execute("SELECT COUNT(*) FROM fact_enrollment WHERE feedback_rating NOT BETWEEN 1 AND 5").fetchone()[0]
        self.assertEqual(n,0)
    def test_quality_issues_detected(self):
        q=pd.read_csv(ROOT/"data"/"processed"/"data_quality_exceptions.csv")
        self.assertGreater(len(q),0)
        self.assertIn("UNKNOWN_EMPLOYEE",set(q.exception_type))
if __name__=="__main__": unittest.main()
