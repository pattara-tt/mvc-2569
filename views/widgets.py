import tkinter as tk
from tkinter import ttk

def make_topbar(parent, title: str, on_logout):
    bar = tk.Frame(parent)
    bar.pack(fill="x", padx=16, pady=(16, 8))

    lbl = tk.Label(bar, text=title, font=("Segoe UI", 16, "bold"))
    lbl.pack(side="left")

    btn = ttk.Button(bar, text="Logout", command=on_logout)
    btn.pack(side="right")
    return bar

def apply_clean_table_style(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("Treeview",
                    borderwidth=0,
                    relief="flat",
                    highlightthickness=0,
                    rowheight=28)
    style.configure("Treeview.Heading",
                    borderwidth=0,
                    relief="flat")
    style.layout("Treeview", [
        ("Treeview.treearea", {"sticky": "nswe"})
    ])
