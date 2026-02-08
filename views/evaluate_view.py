import tkinter as tk
from tkinter import ttk, messagebox
from .base_view import BaseView
from .widgets import make_topbar

class EvaluateView(BaseView):
    def __init__(self, root, app, evaluation_controller):
        super().__init__(root, app)
        self.evaluation_controller = evaluation_controller
        self.student_id = None

        make_topbar(self.frame, "ประเมินความพร้อมจบ", on_logout=self.app.logout)

        body = tk.Frame(self.frame)
        body.pack(fill="both", expand=True, padx=16, pady=8)

        self.info_lbl = tk.Label(body, text="", font=("Segoe UI", 11))
        self.info_lbl.pack(anchor="w", pady=(0, 10))

        box = tk.LabelFrame(body, text="แก้ไขข้อมูลที่ใช้ประเมิน", padx=12, pady=12)
        box.pack(fill="x")

        # credits
        row1 = tk.Frame(box)
        row1.pack(fill="x", pady=4)
        tk.Label(row1, text="หน่วยกิตสะสม", width=16, anchor="w").pack(side="left")
        self.credits_var = tk.StringVar()
        self.credits_entry = ttk.Entry(row1, textvariable=self.credits_var, width=16)
        self.credits_entry.pack(side="left")

        # project
        row2 = tk.Frame(box)
        row2.pack(fill="x", pady=4)
        tk.Label(row2, text="สถานะโครงงาน", width=16, anchor="w").pack(side="left")
        self.project_var = tk.StringVar()
        self.project_cb = ttk.Combobox(row2, textvariable=self.project_var, state="readonly",
                                       values=["ยังไม่ผ่าน", "ผ่านแล้ว"], width=14)
        self.project_cb.pack(side="left")

        # student status
        row3 = tk.Frame(box)
        row3.pack(fill="x", pady=4)
        tk.Label(row3, text="สถานะนักศึกษา", width=16, anchor="w").pack(side="left")
        self.status_var = tk.StringVar()
        self.status_cb = ttk.Combobox(row3, textvariable=self.status_var, state="readonly",
                                      values=["กำลังเรียน", "จบการศึกษา"], width=14)
        self.status_cb.pack(side="left")

        actions = tk.Frame(body)
        actions.pack(fill="x", pady=12)

        self.back_btn = ttk.Button(actions, text="กลับ", command=self.on_back)
        self.back_btn.pack(side="left")

        self.save_btn = ttk.Button(actions, text="บันทึกการแก้ไข", command=self.on_save)
        self.save_btn.pack(side="left", padx=8)

        self.eval_btn = ttk.Button(actions, text="ประเมิน", command=self.on_evaluate)
        self.eval_btn.pack(side="right")

    def show(self, **kwargs):
        super().show(**kwargs)
        self.student_id = kwargs.get("student_id")
        self.load_student()

    def load_student(self):
        try:
            ctx = self.evaluation_controller.get_student_context(self.student_id)
            st = ctx["student"]
            full_name = f"{st['first_name']} {st['last_name']}"
            self.info_lbl.config(text=f"{st['student_id']}  {full_name} | {st['department']} | {st['faculty']}")

            self.credits_var.set(str(ctx["credits"]))
            self.project_var.set(ctx["project_status"])
            self.status_var.set(st["status"])
        except Exception as e:
            messagebox.showerror("ผิดพลาด", str(e))
            self.app.show("students")

    def on_back(self):
        self.app.show("students")

    def on_save(self):
        try:
            credits = int(self.credits_var.get().strip() or "0")
            project = self.project_var.get()
            status = self.status_var.get()

            self.evaluation_controller.update_graduation_fields(self.student_id, credits, project, status)
            messagebox.showinfo("สำเร็จ", "บันทึกแล้ว")
        except Exception as e:
            messagebox.showerror("ผิดพลาด", str(e))

    # ประเมินและไปหน้าผลประเมิน
    def on_evaluate(self):
        try:
            # กันลืมบันทึก
            self.on_save()
            self.evaluation_controller.evaluate_and_save(self.student_id)
        except Exception as e:
            messagebox.showerror("ผิดพลาด", str(e))