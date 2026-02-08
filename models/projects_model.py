from .database import Database

class ProjectsModel:
    def __init__(self, db: Database):
        self.db = db

    def get_project_status(self, student_id: str) -> str:
        with self.db.connect() as conn:
            row = conn.execute("SELECT project_status FROM Projects WHERE student_id = ?", (student_id,)).fetchone()
            return row["project_status"] if row else "ยังไม่ผ่าน"

    def set_project_status(self, student_id: str, project_status: str):
        if project_status not in ("ยังไม่ผ่าน", "ผ่านแล้ว"):
            raise ValueError("สถานะโครงงานไม่ถูก")
        with self.db.connect() as conn:
            # หา project_id เดิม ถ้าไม่มีสร้างใหม่
            row = conn.execute("SELECT project_id FROM Projects WHERE student_id = ? LIMIT 1", (student_id,)).fetchone()
            if row:
                conn.execute(
                    "UPDATE Projects SET project_status = ? WHERE student_id = ?",
                    (project_status, student_id)
                )
            else:
                conn.execute(
                    "INSERT INTO Projects(project_id, student_id, project_status) VALUES(?,?,?)",
                    (f"PJ-{student_id}", student_id, project_status)
                )
            conn.commit()

class ProjectEvaluator:
    def evaluate(self, project_status: str) -> dict:
        passed = (project_status == "ผ่านแล้ว")
        return {
            "passed": passed,
            "detail": f"สถานะโครงงาน: {project_status}"
        }
