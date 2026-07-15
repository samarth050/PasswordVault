"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Audit Log Schema

Purpose :
    Stores application audit events.
===============================================================
"""

from __future__ import annotations

TABLE_NAME = "AuditLog"

CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    event_time TEXT NOT NULL,

    event_type TEXT NOT NULL,

    description TEXT
);
"""

CREATE_INDEXES = [

f"""
CREATE INDEX IF NOT EXISTS
idx_audit_event_time
ON {TABLE_NAME}(event_time);
""",

f"""
CREATE INDEX IF NOT EXISTS
idx_audit_event_type
ON {TABLE_NAME}(event_type);
"""

]