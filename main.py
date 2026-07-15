"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 1.0.0

Module  : Main Entry Point

Purpose :
    Starts VaultX Enterprise.

===============================================================
"""

from __future__ import annotations

import ttkbootstrap as ttk

from gui.login_window import LoginWindow


def main() -> None:
    """
    Application entry point.
    """

    app = ttk.Window(
        title="VaultX Enterprise",
        themename="flatly",
        size=(600, 420),
        resizable=(False, False),
    )

    LoginWindow(app)

    app.mainloop()


if __name__ == "__main__":
    main()