from .database import Database

class StudentModel:
    def __init__(self, db: Database):
        self.db = db

    def list_students(self):
        with self.db.connect() as conn:
            rows = conn.execute("""
                SELECT s.student_id, s.first_name, s.last_name, s.department, s.faculty, s.status,
                       c.total_credits,
                       p.project_status
                FROM Students s
                LEFT JOIN Credits c ON c.student_id = s.student_id
                LEFT JOIN Projects p ON p.student_id = s.student_id
                ORDER BY s.student_id
            """).fetchall()
            return [dict(r) for r in rows]

    def get_student(self, student_id: str):
        with self.db.connect() as conn:
            row = conn.execute("""
                SELECT student_id, first_name, last_name, department, faculty, status
                FROM Students
                WHERE student_id = ?
            """, (student_id,)).fetchone()
            return dict(row) if row else None

    # แก้สถานะการเรียน
    def set_status(self, student_id: str, status: str):
        if status not in ("กำลังเรียน", "จบการศึกษา"):
            raise ValueError("สถานะนักศึกษาไม่ถูก")
        with self.db.connect() as conn:
            conn.execute("UPDATE Students SET status = ? WHERE student_id = ?", (status, student_id))
            conn.commit()
