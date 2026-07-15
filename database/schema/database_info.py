"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : DatabaseInfo Schema

Purpose :
    Database metadata and version tracking.
===============================================================
"""

from __future__ import annotations

TABLE_NAME = "DatabaseInfo"

CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    id INTEGER PRIMARY KEY CHECK(id = 1),

    database_version INTEGER NOT NULL,

    encryption_version INTEGER NOT NULL,

    application_version TEXT NOT NULL,

    created_on TEXT NOT NULL,

    last_upgrade TEXT
);
"""

CREATE_INDEXES: list[str] = []