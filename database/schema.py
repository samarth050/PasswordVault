"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Module  : Database Schema
Purpose : Defines SQLite schema, indexes, default values,
          and database version information.
===============================================================
"""

from pathlib import Path

# ===============================================================
# Application Information
# ===============================================================

APP_NAME = "VaultX Enterprise"
APP_VERSION = "0.1.0"

# ===============================================================
# Database Information
# ===============================================================

DATABASE_NAME = "vault.db"
DATABASE_VERSION = 1
ENCRYPTION_VERSION = 1

DATABASE_PATH = Path(DATABASE_NAME)

# ===============================================================
# Table Names
# ===============================================================

TABLE_DATABASE_INFO = "DatabaseInfo"
TABLE_USERS = "Users"
TABLE_VAULTS = "Vaults"
TABLE_CATEGORIES = "Categories"
TABLE_VAULT_ITEMS = "VaultItems"
TABLE_PASSWORD_HISTORY = "PasswordHistory"
TABLE_AUDIT_LOG = "AuditLog"
TABLE_APPLICATION_SETTINGS = "ApplicationSettings"

# ===============================================================
# Default Categories
# ===============================================================

DEFAULT_CATEGORIES = [
    "Banking",
    "Cloud",
    "Development",
    "Email",
    "Finance",
    "Government",
    "Investment",
    "Medical",
    "Office",
    "Shopping",
    "Social",
    "Travel",
    "Utilities",
    "Others"
]

# ===============================================================
# DatabaseInfo
# ===============================================================

CREATE_DATABASE_INFO_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_DATABASE_INFO}
(
    id INTEGER PRIMARY KEY CHECK(id=1),

    database_version INTEGER NOT NULL,

    created_on TEXT NOT NULL,

    last_upgrade TEXT,

    encryption_version INTEGER NOT NULL
);
"""

# ===============================================================
# Users
# ===============================================================

CREATE_USERS_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_USERS}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,

    password_hash TEXT NOT NULL,

    salt TEXT NOT NULL,

    display_name TEXT,

    email TEXT,

    created_on TEXT NOT NULL,

    last_login TEXT,

    active INTEGER DEFAULT 1
);
"""

# ===============================================================
# Vaults
# ===============================================================

CREATE_VAULTS_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_VAULTS}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    vault_name TEXT NOT NULL,

    description TEXT,

    created_on TEXT NOT NULL,

    FOREIGN KEY(user_id)
        REFERENCES Users(id)
);
"""

# ===============================================================
# Categories
# ===============================================================

CREATE_CATEGORIES_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_CATEGORIES}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    category_name TEXT NOT NULL UNIQUE
);
"""

# ===============================================================
# Vault Items
# ===============================================================

CREATE_VAULT_ITEMS_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_VAULT_ITEMS}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    vault_id INTEGER NOT NULL,

    category_id INTEGER,

    website TEXT NOT NULL,

    url TEXT,

    username TEXT,

    password TEXT,

    notes TEXT,

    favorite INTEGER DEFAULT 0,

    created_on TEXT,

    modified_on TEXT,

    FOREIGN KEY(vault_id)
        REFERENCES Vaults(id),

    FOREIGN KEY(category_id)
        REFERENCES Categories(id)
);
"""

# ===============================================================
# Password History
# ===============================================================

CREATE_PASSWORD_HISTORY_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_PASSWORD_HISTORY}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    vault_item_id INTEGER NOT NULL,

    encrypted_password TEXT NOT NULL,

    changed_on TEXT NOT NULL,

    FOREIGN KEY(vault_item_id)
        REFERENCES VaultItems(id)
);
"""

# ===============================================================
# Audit Log
# ===============================================================

CREATE_AUDIT_LOG_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_AUDIT_LOG}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    event_time TEXT NOT NULL,

    event_type TEXT NOT NULL,

    description TEXT
);
"""

# ===============================================================
# Application Settings
# ===============================================================

CREATE_APPLICATION_SETTINGS_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_APPLICATION_SETTINGS}
(
    setting_name TEXT PRIMARY KEY,

    setting_value TEXT
);
"""

# ===============================================================
# Indexes
# ===============================================================

CREATE_INDEXES = [

"""
CREATE INDEX IF NOT EXISTS idx_vault_items_website
ON VaultItems(website);
""",

"""
CREATE INDEX IF NOT EXISTS idx_vault_items_favorite
ON VaultItems(favorite);
""",

"""
CREATE INDEX IF NOT EXISTS idx_categories_name
ON Categories(category_name);
"""

]