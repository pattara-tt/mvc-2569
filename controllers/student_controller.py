class StudentController:
    def __init__(self, app, student_model):
        self.app = app
        self.student_model = student_model

    def require_admin(self):
        if self.app.session.get("role") != "admin":
            raise ValueError("ไม่มีสิทธิ์เข้าถึง")
        
    # ดึงข้อมูลนักศึกษา
    def list_students(self):
        self.require_admin()
        return self.student_model.list_students()

    # เปิดหน้าประเมิน
    def open_evaluate(self, student_id: str):
        self.require_admin()
        self.app.show("evaluate", student_id=student_id)
