from models.validator import Validator

class AuthController:
    def __init__(self, app, user_model):
        self.app = app
        self.user_model = user_model

    def handle_login(self, email: str):
        email = Validator.validate_email(email)
        role = self.user_model.get_role_by_email(email)
        if role != "admin":
            raise ValueError("email นี้ไม่ใช่ admin")
        self.app.login(email, role)
        self.app.show("students")
