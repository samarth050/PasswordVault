"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 1.0.0

Module  : Login Window

===============================================================
"""

from __future__ import annotations

import ttkbootstrap as ttk

from ttkbootstrap.constants import *

from services.auth_service import AuthService

from gui.create_admin_dialog import CreateAdminDialog

from gui.main_window import MainWindow

class LoginWindow:

    def __init__(self, master):

        self.master = master

        self.auth = AuthService()

        self.username = ttk.StringVar(value="admin")

        self.password = ttk.StringVar()

        self.build_ui()

        if self.auth.is_first_run():

            self.master.after(

                200,

                lambda: CreateAdminDialog(self.master)

            )        

    # -----------------------------------------------------

    def build_ui(self):

        frame = ttk.Frame(
            self.master,
            padding=20,
        )

        frame.pack(
            fill=BOTH,
            expand=True,
        )

        ttk.Label(
            frame,
            text="VaultX Enterprise",
            font=("Segoe UI", 20, "bold"),
        ).pack(
            pady=(10, 30)
        )

        #
        # Username
        #

        ttk.Label(
            frame,
            text="Username",
        ).pack(anchor=W)

        ttk.Entry(
            frame,
            textvariable=self.username,
            width=35,
        ).pack(
            pady=(0, 15)
        )

        #
        # Password
        #

        ttk.Label(
            frame,
            text="Master Password",
        ).pack(anchor=W)

        ttk.Entry(
            frame,
            textvariable=self.password,
            show="•",
            width=35,
        ).pack(
            pady=(0, 20)
        )

        #
        # Buttons
        #

        button_frame = ttk.Frame(frame)

        button_frame.pack()

        ttk.Button(
            button_frame,
            text="Login",
            bootstyle="success",
            width=15,
            command=self.login,
        ).grid(
            row=0,
            column=0,
            padx=5,
        )

        ttk.Button(
            button_frame,
            text="Exit",
            bootstyle="danger",
            width=15,
            command=self.master.destroy,
        ).grid(
            row=0,
            column=1,
            padx=5,
        )

        #
        # Status
        #

        self.status = ttk.Label(
            frame,
            text="",
            bootstyle="danger",
        )

        self.status.pack(
            pady=20
        )

    # -----------------------------------------------------

    def login(self):

        #
        # First Run?
        #

        if self.auth.is_first_run():

            CreateAdminDialog(self.master)

            return

        success, _ = self.auth.authenticate(

            self.username.get(),

            self.password.get()

        )

        if success:

            self.master.destroy()

            app = MainWindow()

            app.show()

        else:

            self.status.configure(

                text="Invalid username or password.",

                bootstyle="danger"

            )