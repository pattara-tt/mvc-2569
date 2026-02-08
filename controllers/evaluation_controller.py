class EvaluationController:
    def __init__(self, app, student_model, credits_model, projects_model, evaluator, result_model):
        self.app = app
        self.student_model = student_model
        self.credits_model = credits_model
        self.projects_model = projects_model
        self.evaluator = evaluator
        self.result_model = result_model

    def require_admin(self):
        if self.app.session.get("role") != "admin":
            raise ValueError("คุณไม่มีสิทธิ์")

    # โหลดข้อมูลนักศึกษา
    def get_student_context(self, student_id: str):
        self.require_admin()
        student = self.student_model.get_student(student_id)
        if not student:
            raise ValueError("ไม่พบนักศึกษา")

        credits = self.credits_model.get_total_credits(student_id)
        project_status = self.projects_model.get_project_status(student_id)

        return {
            "student": student,
            "credits": credits,
            "project_status": project_status
        }

    # update การเเก้ไขข้อมูล
    def update_graduation_fields(self, student_id: str, total_credits: int, project_status: str, student_status: str):
        self.require_admin()
        self.credits_model.set_total_credits(student_id, total_credits)
        self.projects_model.set_project_status(student_id, project_status)
        self.student_model.set_status(student_id, student_status)

    # ประเมินจบ
    def evaluate_and_save(self, student_id: str):
        self.require_admin()
        data = self.evaluator.evaluate(student_id)
        self.result_model.save_result(student_id, data["result_text"], data["evaluated_at"])
        self.app.show("result", student_id=student_id, result=data)
