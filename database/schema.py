"""
SQLite Database Schema
"""

DATABASE_NAME = "vault.db"

CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS Settings
(
    id INTEGER PRIMARY KEY CHECK(id=1),

    password_hash TEXT NOT NULL,

    salt TEXT NOT NULL,

    created_on TEXT NOT NULL
);
"""

CREATE_VAULT_TABLE = """
CREATE TABLE IF NOT EXISTS Vault
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    website TEXT,

    url TEXT,

    username TEXT,

    password TEXT,

    category TEXT,

    notes TEXT,

    favorite INTEGER DEFAULT 0,

    created_on TEXT,

    modified_on TEXT
);
"""

CREATE_INDEX1 = """
CREATE INDEX IF NOT EXISTS idx_website
ON Vault(website);
"""

CREATE_INDEX2 = """
CREATE INDEX IF NOT EXISTS idx_category
ON Vault(category);
"""