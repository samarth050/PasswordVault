"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Vaults Schema

Purpose :
    Stores user vaults.
===============================================================
"""

from __future__ import annotations

TABLE_NAME = "Vaults"

CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    vault_name TEXT NOT NULL,

    description TEXT,

    created_on TEXT NOT NULL,

    FOREIGN KEY(user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE
);
"""

CREATE_INDEXES = [

f"""
CREATE INDEX IF NOT EXISTS
idx_vaults_user
ON {TABLE_NAME}(user_id);
""",

f"""
CREATE UNIQUE INDEX IF NOT EXISTS
idx_vaults_name
ON {TABLE_NAME}(user_id, vault_name);
"""

]