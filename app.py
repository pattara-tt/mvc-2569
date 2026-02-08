import tkinter as tk

from models.database import Database
from models.user_model import UserModel
from models.student_model import StudentModel
from models.credits_model import CreditsModel
from models.projects_model import ProjectsModel
from models.graduation_model import GraduationEvaluator, GraduationResultModel

from controllers.app_controller import AppController
from controllers.auth_controller import AuthController
from controllers.student_controller import StudentController
from controllers.evaluation_controller import EvaluationController

from views.widgets import apply_clean_table_style
from views.login_view import LoginView
from views.students_view import StudentsListView
from views.evaluate_view import EvaluateView
from views.result_view import ResultView


class GraduationMVCApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ระบบประเมินความพร้อมจบ")
        self.root.geometry("900x520")
        self.root.minsize(820, 480)

        apply_clean_table_style(self.root)

        self.db = Database("app.db")
        self.db.init_schema()
        self.db.seed_data()

        self.user_model = UserModel(self.db)
        self.student_model = StudentModel(self.db)
        self.credits_model = CreditsModel(self.db)
        self.projects_model = ProjectsModel(self.db)

        self.result_model = GraduationResultModel(self.db)
        self.evaluator = GraduationEvaluator(self.credits_model, self.projects_model)

        self.app = AppController(self.root, views={})

        self.auth_controller = AuthController(self.app, self.user_model)
        self.student_controller = StudentController(self.app, self.student_model)
        self.evaluation_controller = EvaluationController(
            self.app,
            self.student_model,
            self.credits_model,
            self.projects_model,
            self.evaluator,
            self.result_model
        )

        self.views = {
            "login": LoginView(self.root, self.app, self.auth_controller),
            "students": StudentsListView(self.root, self.app, self.student_controller),
            "evaluate": EvaluateView(self.root, self.app, self.evaluation_controller),
            "result": ResultView(self.root, self.app),
        }
        self.app.views = self.views

    def run(self):
        self.app.show("login")
        self.root.mainloop()
