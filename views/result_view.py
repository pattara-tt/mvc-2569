import tkinter as tk
from tkinter import ttk
from .base_view import BaseView
from .widgets import make_topbar

class ResultView(BaseView):
    def __init__(self, root, app):
        super().__init__(root, app)
        self.student_id = None
        self.result = None

        make_topbar(self.frame, "ผลการประเมิน", on_logout=self.app.logout)

        body = tk.Frame(self.frame)
        body.pack(fill="both", expand=True, padx=16, pady=8)

        self.summary_lbl = tk.Label(body, text="", font=("Segoe UI", 14, "bold"))
        self.summary_lbl.pack(anchor="w", pady=(0, 10))

        self.detail_lbl = tk.Label(body, text="", font=("Segoe UI", 10), justify="left")
        self.detail_lbl.pack(anchor="w")

        self.time_lbl = tk.Label(body, text="", font=("Segoe UI", 9))
        self.time_lbl.pack(anchor="w", pady=(10, 0))

        actions = tk.Frame(body)
        actions.pack(fill="x", pady=16)

        self.back_btn = ttk.Button(actions, text="กลับไปรายชื่อนักศึกษา", command=self.on_back)
        self.back_btn.pack(side="right")

    def show(self, **kwargs):
        super().show(**kwargs)
        self.student_id = kwargs.get("student_id")
        self.result = kwargs.get("result")

        if not self.result:
            self.summary_lbl.config(text="ไม่พบผลการประเมิน")
            self.detail_lbl.config(text="")
            self.time_lbl.config(text="")
            return

        self.summary_lbl.config(text=self.result["summary"])
        d1 = self.result["credit"]["detail"]
        d2 = self.result["project"]["detail"]
        self.detail_lbl.config(text=f"{d1}\n{d2}")
        self.time_lbl.config(text=f"ประเมินเมื่อ: {self.result['evaluated_at']}")

    def on_back(self):
        self.app.show("students")
