import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseView
from .widgets import make_topbar

class StudentsListView(BaseView):
    def __init__(self, root, app, student_controller):
        super().__init__(root, app)
        self.student_controller = student_controller

        self.frame.configure(padx=0, pady=0)

        make_topbar(self.frame, "รายชื่อนักศึกษา", on_logout=self.app.logout)

        body = tk.Frame(self.frame)
        body.pack(fill="both", expand=True, padx=16, pady=8)

        actions = tk.Frame(body)
        actions.pack(fill="x", pady=(0, 8))

        self.refresh_btn = ttk.Button(actions, text="refresh", command=self.refresh)
        self.refresh_btn.pack(side="left")

        self.eval_btn = ttk.Button(actions, text="evaluate", command=self.on_evaluate)
        self.eval_btn.pack(side="right")

        cols = ("student_id", "name", "department", "credits", "project", "ready")
        self.table = ttk.Treeview(body, columns=cols, show="headings", height=12)

        self.table.heading("student_id", text="รหัส")
        self.table.heading("name", text="ชื่อ-นามสกุล")
        self.table.heading("department", text="ภาควิชา")
        self.table.heading("credits", text="หน่วยกิต")
        self.table.heading("project", text="โครงงาน")
        self.table.heading("ready", text="สถานะพร้อมจบ")

        self.table.column("student_id", width=90, anchor="w")
        self.table.column("name", width=160, anchor="w")
        self.table.column("department", width=170, anchor="w")
        self.table.column("credits", width=70, anchor="center")
        self.table.column("project", width=80, anchor="center")
        self.table.column("ready", width=110, anchor="center")

        self.table.pack(fill="both", expand=True)

    def show(self, **kwargs):
        super().show(**kwargs)
        self.refresh()

    def refresh(self):
        try:
            rows = self.student_controller.list_students()
            for item in self.table.get_children():
                self.table.delete(item)

            for r in rows:
                name = f"{r['first_name']} {r['last_name']}"
                credits = r.get("total_credits", 0) if r.get("total_credits") is not None else 0
                project = r.get("project_status") or "ยังไม่ผ่าน"

                ready = "ไม่ทราบ"
                if credits >= 135 and project == "ผ่านแล้ว":
                    ready = "พร้อม"
                else:
                    ready = "ยังไม่พร้อม"

                self.table.insert("", "end", values=(
                    r["student_id"], name, r["department"], credits, project, ready
                ))
        except Exception as e:
            messagebox.showerror("ผิดพลาด", str(e))

    # เปิดหน้าประเมิน
    def on_evaluate(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("เลือกก่อน", "เลือกนักศึกษาก่อน")
            return
        values = self.table.item(selected[0], "values")
        student_id = values[0]
        try:
            self.student_controller.open_evaluate(student_id)
        except Exception as e:
            messagebox.showerror("ผิดพลาด", str(e))
