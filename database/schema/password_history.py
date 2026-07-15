"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Password History Schema

Purpose :
    Maintains history of password changes.
===============================================================
"""

from __future__ import annotations

TABLE_NAME = "PasswordHistory"

CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    vault_item_id INTEGER NOT NULL,

    encrypted_password TEXT NOT NULL,

    changed_on TEXT NOT NULL,

    FOREIGN KEY(vault_item_id)
        REFERENCES VaultItems(id)
        ON DELETE CASCADE
);
"""

CREATE_INDEXES = [

f"""
CREATE INDEX IF NOT EXISTS
idx_history_item
ON {TABLE_NAME}(vault_item_id);
"""

]