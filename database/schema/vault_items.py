"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Vault Items Schema

Purpose :
    Stores all passwords and credentials.
===============================================================
"""

from __future__ import annotations

TABLE_NAME = "VaultItems"

CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    vault_id INTEGER NOT NULL,

    category_id INTEGER,

    website TEXT NOT NULL,

    url TEXT,

    username TEXT,

    password TEXT,

    notes TEXT,

    favorite INTEGER NOT NULL DEFAULT 0,

    created_on TEXT NOT NULL,

    modified_on TEXT NOT NULL,

    FOREIGN KEY(vault_id)
        REFERENCES Vaults(id)
        ON DELETE CASCADE,

    FOREIGN KEY(category_id)
        REFERENCES Categories(id)
);
"""

CREATE_INDEXES = [

f"""
CREATE INDEX IF NOT EXISTS
idx_items_vault
ON {TABLE_NAME}(vault_id);
""",

f"""
CREATE INDEX IF NOT EXISTS
idx_items_category
ON {TABLE_NAME}(category_id);
""",

f"""
CREATE INDEX IF NOT EXISTS
idx_items_website
ON {TABLE_NAME}(website);
""",

f"""
CREATE INDEX IF NOT EXISTS
idx_items_favorite
ON {TABLE_NAME}(favorite);
"""

]