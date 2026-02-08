from .database import Database

class UserModel:
    def __init__(self, db: Database):
        self.db = db

    def get_role_by_email(self, email: str):
        with self.db.connect() as conn:
            row = conn.execute("SELECT role FROM Users WHERE email = ?", (email,)).fetchone()
            return row["role"] if row else None
