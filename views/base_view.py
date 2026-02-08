import tkinter as tk

class BaseView:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(root)

    def show(self, **kwargs):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
