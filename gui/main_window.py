"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Main Application Window
===============================================================
"""

from __future__ import annotations

import ttkbootstrap as ttk

from ttkbootstrap.constants import *


class MainWindow:

    def __init__(self):

        self.window = ttk.Window(
            title="VaultX Enterprise",
            themename="flatly",
            size=(1400, 800),
        )

        self.window.minsize(1200, 700)

        self.search_text = ttk.StringVar()

        self.build_menu()

        self.build_toolbar()

        self.build_body()

        self.build_statusbar()

    # ---------------------------------------------------------

    def show(self):

        self.window.mainloop()

    # ---------------------------------------------------------

    def build_menu(self):

        menu = ttk.Menu(self.window)

        file_menu = ttk.Menu(menu, tearoff=False)

        file_menu.add_command(label="New")

        file_menu.add_command(label="Backup")

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.window.destroy
        )

        menu.add_cascade(label="File", menu=file_menu)

        edit_menu = ttk.Menu(menu, tearoff=False)

        edit_menu.add_command(label="Add")

        edit_menu.add_command(label="Edit")

        edit_menu.add_command(label="Delete")

        menu.add_cascade(label="Edit", menu=edit_menu)

        tools_menu = ttk.Menu(menu, tearoff=False)

        tools_menu.add_command(label="Settings")

        menu.add_cascade(label="Tools", menu=tools_menu)

        help_menu = ttk.Menu(menu, tearoff=False)

        help_menu.add_command(label="About")

        menu.add_cascade(label="Help", menu=help_menu)

        self.window.config(menu=menu)

    # ---------------------------------------------------------

    def build_toolbar(self):

        toolbar = ttk.Frame(self.window, padding=5)

        toolbar.pack(fill=X)

        buttons = [

            "New",

            "Edit",

            "Delete",

            "Copy Username",

            "Copy Password",

            "Backup"

        ]

        for text in buttons:

            ttk.Button(

                toolbar,

                text=text,

                width=15

            ).pack(

                side=LEFT,

                padx=2

            )

    # ---------------------------------------------------------

    def build_body(self):

        paned = ttk.PanedWindow(
            self.window,
            orient=HORIZONTAL
        )

        paned.pack(fill=BOTH, expand=True)

        #
        # Left Panel
        #

        left = ttk.Frame(
            paned,
            padding=10,
            width=250
        )

        ttk.Label(

            left,

            text="Categories",

            font=("Segoe UI", 11, "bold")

        ).pack(anchor=W)

        self.category_list = ttk.Treeview(

            left,

            show="tree",

            height=25

        )

        self.category_list.pack(

            fill=BOTH,

            expand=True,

            pady=5

        )

        self.category_list.insert("", END, text="All")

        self.category_list.insert("", END, text="Banking")

        self.category_list.insert("", END, text="Email")

        self.category_list.insert("", END, text="Shopping")

        paned.add(left, weight=1)

        #
        # Center Panel
        #

        center = ttk.Frame(
            paned,
            padding=10
        )

        search_frame = ttk.Frame(center)

        search_frame.pack(fill=X)

        ttk.Label(

            search_frame,

            text="Search"

        ).pack(side=LEFT)

        ttk.Entry(

            search_frame,

            textvariable=self.search_text,

            width=40

        ).pack(

            side=LEFT,

            padx=5

        )

        columns = (

            "Website",

            "Username",

            "Category",

        )

        self.tree = ttk.Treeview(

            center,

            columns=columns,

            show="headings"

        )

        for col in columns:

            self.tree.heading(

                col,

                text=col

            )

            self.tree.column(

                col,

                width=180

            )

        self.tree.pack(

            fill=BOTH,

            expand=True,

            pady=10

        )

        paned.add(center, weight=3)

        #
        # Right Panel
        #

        right = ttk.LabelFrame(

            paned,

            text="Details",

            padding=10,

            width=350

        )

        fields = [

            "Website",

            "URL",

            "Username",

            "Password",

            "Category",

            "Notes"

        ]

        for field in fields:

            ttk.Label(

                right,

                text=field

            ).pack(anchor=W)

            ttk.Entry(

                right,

                width=35

            ).pack(

                pady=(0, 8)

            )

        paned.add(right, weight=2)

    # ---------------------------------------------------------

    def build_statusbar(self):

        self.status = ttk.Label(

            self.window,

            text="Ready",

            relief="sunken",

            anchor=W

        )

        self.status.pack(fill=X)