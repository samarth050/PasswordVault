"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 1.0.0

Module  : Create Administrator Dialog
===============================================================
"""

from __future__ import annotations

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

from services.auth_service import AuthService


class CreateAdminDialog:

    def __init__(self, parent):

        self.parent = parent
        self.auth = AuthService()

        self.window = ttk.Toplevel(parent)

        self.window.title("Create Administrator")
        self.window.geometry("650x600")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self.username = ttk.StringVar(value="admin")
        self.display_name = ttk.StringVar(value="Administrator")
        self.email = ttk.StringVar()

        self.password = ttk.StringVar()
        self.confirm_password = ttk.StringVar()

        self.show_password = ttk.BooleanVar(value=False)

        self.build_ui()

        self.window.bind("<Return>", lambda e: self.create_admin())
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    # ---------------------------------------------------------

    def build_ui(self):

        frame = ttk.Frame(
            self.window,
            padding=20
        )

        frame.pack(fill=BOTH, expand=True)

        ttk.Label(
            frame,
            text="Create Administrator Account",
            font=("Segoe UI", 18, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            pady=(0, 20)
        )

        row = 1

        self.add_row(frame, row, "Username", self.username)
        row += 1

        self.add_row(frame, row, "Display Name", self.display_name)
        row += 1

        self.add_row(frame, row, "Email", self.email)
        row += 1

        self.password_entry = self.add_row(
            frame,
            row,
            "Master Password",
            self.password,
            show="•"
        )

        row += 1

        self.confirm_entry = self.add_row(
            frame,
            row,
            "Confirm Password",
            self.confirm_password,
            show="•"
        )

        row += 1

        ttk.Checkbutton(
            frame,
            text="Show Passwords",
            variable=self.show_password,
            command=self.toggle_password
        ).grid(
            row=row,
            column=1,
            sticky=W,
            pady=(10, 5)
        )

        row += 1

        ttk.Label(
            frame,
            text="Password Strength:"
        ).grid(
            row=row,
            column=0,
            sticky=E,
            pady=10
        )

        self.strength = ttk.Label(
            frame,
            text="",
            bootstyle="secondary"
        )

        self.strength.grid(
            row=row,
            column=1,
            sticky=W
        )

        self.password.trace_add(
            "write",
            lambda *_: self.update_strength()
        )

        row += 1

        button_frame = ttk.Frame(frame)

        button_frame.grid(
            row=row,
            column=0,
            columnspan=3,
            pady=25
        )

        ttk.Button(
            button_frame,
            text="Create Vault",
            bootstyle="success",
            width=18,
            command=self.create_admin
        ).pack(
            side=LEFT,
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Cancel",
            bootstyle="secondary",
            width=18,
            command=self.window.destroy
        ).pack(
            side=LEFT,
            padx=5
        )

    # ---------------------------------------------------------

    def add_row(
        self,
        parent,
        row,
        text,
        variable,
        show=""
    ):

        ttk.Label(
            parent,
            text=text
        ).grid(
            row=row,
            column=0,
            sticky=E,
            padx=(0, 10),
            pady=8
        )

        entry = ttk.Entry(
            parent,
            textvariable=variable,
            width=35,
            show=show
        )

        entry.grid(
            row=row,
            column=1,
            sticky=W
        )

        return entry

    # ---------------------------------------------------------

    def toggle_password(self):

        char = "" if self.show_password.get() else "•"

        self.password_entry.configure(show=char)

        self.confirm_entry.configure(show=char)

    # ---------------------------------------------------------

    def update_strength(self):

        password = self.password.get()

        score = 0

        if len(password) >= 8:
            score += 1

        if any(c.islower() for c in password):
            score += 1

        if any(c.isupper() for c in password):
            score += 1

        if any(c.isdigit() for c in password):
            score += 1

        if any(not c.isalnum() for c in password):
            score += 1

        levels = {
            0: ("Very Weak", "danger"),
            1: ("Weak", "danger"),
            2: ("Fair", "warning"),
            3: ("Good", "info"),
            4: ("Strong", "success"),
            5: ("Excellent", "success")
        }

        text, style = levels[score]

        self.strength.configure(
            text=text,
            bootstyle=style
        )

    # ---------------------------------------------------------

    def create_admin(self):

        if self.password.get() != self.confirm_password.get():

            messagebox.showerror(
                "Error",
                "Passwords do not match."
            )

            return

        if len(self.password.get()) < 8:

            messagebox.showerror(
                "Error",
                "Password must be at least 8 characters."
            )

            return

        created = self.auth.create_admin_user(

            username=self.username.get(),

            master_password=self.password.get(),

            display_name=self.display_name.get(),

            email=self.email.get()

        )

        if not created:

            messagebox.showerror(
                "Error",
                "Administrator already exists."
            )

            return

        messagebox.showinfo(
            "Success",
            "Administrator account created successfully."
        )

        self.window.destroy()