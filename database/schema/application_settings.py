"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Application Settings Schema

Purpose :
    Stores configurable application settings.
===============================================================
"""

from __future__ import annotations

TABLE_NAME = "ApplicationSettings"

DEFAULT_APPLICATION_SETTINGS = {

    "theme": "light",

    "auto_lock_minutes": "5",

    "clipboard_timeout": "20",

    "window_width": "1200",

    "window_height": "750"

}

CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    setting_name TEXT PRIMARY KEY,

    setting_value TEXT NOT NULL
);
"""

CREATE_INDEXES: list[str] = []