import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseView

class LoginView(BaseView):
    def __init__(self, root, app, auth_controller):
        super().__init__(root, app)
        self.auth_controller = auth_controller

        self.frame.configure(padx=24, pady=24)

        card = tk.Frame(self.frame)
        card.pack(expand=True)

        title = tk.Label(card, text="Login", font=("Segoe UI", 18, "bold"))
        title.pack(pady=(0, 12))

        tk.Label(card, text="Email", font=("Segoe UI", 10)).pack(anchor="w")
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(card, textvariable=self.email_var, width=36)
        self.email_entry.pack(pady=(4, 12), fill="x")

        self.login_btn = ttk.Button(card, text="เข้าสู่ระบบ", command=self.on_login)
        self.login_btn.pack(fill="x")

    def show(self, **kwargs):
        super().show(**kwargs)
        self.email_entry.focus_set()

    def on_login(self):
        try:
            self.auth_controller.handle_login(self.email_var.get())
        except Exception as e:
            messagebox.showerror("Login ไม่สำเร็จ", str(e))
