from datetime import datetime
from .database import Database
from .credits_model import CreditsModel, CreditEvaluator
from .projects_model import ProjectsModel, ProjectEvaluator

class GraduationResultModel:
    def __init__(self, db: Database):
        self.db = db

    def save_result(self, student_id: str, result_text: str, evaluated_at: str):
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO GraduationResults(student_id, result_text, evaluated_at) VALUES(?,?,?)",
                (student_id, result_text, evaluated_at)
            )
            conn.commit()

    def get_latest_result(self, student_id: str):
        with self.db.connect() as conn:
            row = conn.execute("""
                SELECT result_text, evaluated_at
                FROM GraduationResults
                WHERE student_id = ?
                ORDER BY result_id DESC
                LIMIT 1
            """, (student_id,)).fetchone()
            return dict(row) if row else None

class GraduationEvaluator:
    def __init__(self, credits_model: CreditsModel, projects_model: ProjectsModel):
        self.credits_model = credits_model
        self.projects_model = projects_model
        self.credit_eval = CreditEvaluator()
        self.project_eval = ProjectEvaluator()

    def evaluate(self, student_id: str) -> dict:
        total_credits = self.credits_model.get_total_credits(student_id)
        project_status = self.projects_model.get_project_status(student_id)

        credit_result = self.credit_eval.evaluate(total_credits)
        project_result = self.project_eval.evaluate(project_status)

        passed_all = credit_result["passed"] and project_result["passed"]

        lines = []
        lines.append(credit_result["detail"])
        lines.append(project_result["detail"])

        if passed_all:
            summary = "ผ่านการประเมิน: พร้อมจบ"
        else:
            summary = "ไม่ผ่านการประเมิน: ยังไม่พร้อมจบ"

        result_text = summary + " | " + " , ".join(lines)

        return {
            "passed": passed_all,
            "credit": credit_result,
            "project": project_result,
            "summary": summary,
            "result_text": result_text,
            "evaluated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
