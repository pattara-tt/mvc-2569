from .database import Database

class CreditsModel:
    def __init__(self, db: Database):
        self.db = db

    def get_total_credits(self, student_id: str) -> int:
        with self.db.connect() as conn:
            row = conn.execute("SELECT total_credits FROM Credits WHERE student_id = ?", (student_id,)).fetchone()
            return int(row["total_credits"]) if row else 0

    def set_total_credits(self, student_id: str, total_credits: int):
        total_credits = int(total_credits)
        if total_credits < 0:
            raise ValueError("หน่วยกิตต้องไม่ติดลบ")
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO Credits(student_id, total_credits) VALUES(?,?) "
                "ON CONFLICT(student_id) DO UPDATE SET total_credits=excluded.total_credits",
                (student_id, total_credits)
            )
            conn.commit()

class CreditEvaluator:
    MIN_CREDITS = 135
    # ตรวจหน่วยกิตผ่านเกณฑ์
    def evaluate(self, total_credits: int) -> dict:
        passed = total_credits >= self.MIN_CREDITS
        return {
            "passed": passed,
            "detail": f"หน่วยกิตสะสม {total_credits} / {self.MIN_CREDITS}"
        }
