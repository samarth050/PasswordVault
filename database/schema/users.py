"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Users Schema

Purpose :
    Stores application users.
===============================================================
"""

from __future__ import annotations

TABLE_NAME = "Users"

CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    salt TEXT NOT NULL,

    display_name TEXT,

    email TEXT,

    created_on TEXT NOT NULL,

    last_login TEXT,

    active INTEGER NOT NULL DEFAULT 1
);
"""

CREATE_INDEXES = [

f"""
CREATE UNIQUE INDEX IF NOT EXISTS
idx_users_username
ON {TABLE_NAME}(username);
"""

]