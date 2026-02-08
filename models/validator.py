import re

class Validator:
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    @staticmethod
    def validate_email(email: str) -> str:
        email = (email or "").strip()
        if not email:
            raise ValueError("กรอก email ก่อน")
        if not Validator.EMAIL_RE.match(email):
            raise ValueError("รูปแบบ email ไม่ถูก")
        return email
