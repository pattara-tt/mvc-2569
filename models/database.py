import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # สร้างตาราง
    def init_schema(self):
        with self.connect() as conn:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    email TEXT PRIMARY KEY,
                    role TEXT NOT NULL CHECK(role IN ('admin','student'))
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS Students (
                    student_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    faculty TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('กำลังเรียน','จบการศึกษา'))
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS Credits (
                    student_id TEXT PRIMARY KEY,
                    total_credits INTEGER NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES Students(student_id)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS Projects (
                    project_id TEXT PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    project_status TEXT NOT NULL CHECK(project_status IN ('ยังไม่ผ่าน','ผ่านแล้ว')),
                    FOREIGN KEY(student_id) REFERENCES Students(student_id)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS GraduationResults (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    result_text TEXT NOT NULL,
                    evaluated_at TEXT NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES Students(student_id)
                )
            """)

            conn.commit()

    def seed_data(self):
        with self.connect() as conn:
            cur = conn.cursor()

            # ใส่ข้อมูล
            # users
            cur.execute("INSERT OR IGNORE INTO Users(email, role) VALUES(?,?)", ("admin@kmitl.ac.th", "admin"))

            # students
            students = [
                ("65010001", "Pattara", "Uongi", "Software Engineering", "Engineering", "กำลังเรียน"),
                ("65010002", "Narin", "Sukjai", "Computer Science", "Science", "กำลังเรียน"),
                ("65010003", "Suda", "Koom", "Information Tech", "IT", "กำลังเรียน"),
                ("65010004", "Kawin", "Manee", "Software Engineering", "Engineering", "กำลังเรียน"),
                ("65010005", "Pim", "Chaiyo", "Computer Science", "Science", "กำลังเรียน"),
            ]
            cur.executemany("""
                INSERT OR IGNORE INTO Students(student_id, first_name, last_name, department, faculty, status)
                VALUES(?,?,?,?,?,?)
            """, students)

            # credits
            credits = [
                ("65010001", 140),
                ("65010002", 120),
                ("65010003", 135),
                ("65010004", 160),
                ("65010005", 134),
            ]
            cur.executemany("INSERT OR IGNORE INTO Credits(student_id, total_credits) VALUES(?,?)", credits)

            # projects
            projects = [
                ("PJ-001", "65010001", "ผ่านแล้ว"),
                ("PJ-002", "65010002", "ผ่านแล้ว"),
                ("PJ-003", "65010003", "ยังไม่ผ่าน"),
                ("PJ-004", "65010004", "ผ่านแล้ว"),
                ("PJ-005", "65010005", "ยังไม่ผ่าน"),
            ]
            cur.executemany("INSERT OR IGNORE INTO Projects(project_id, student_id, project_status) VALUES(?,?,?)", projects)

            conn.commit()
