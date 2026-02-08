import tkinter as tk

class BaseView:
    # ใช้เก็บ window หลักและสร้าง frame
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(root)

    def show(self, **kwargs):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
