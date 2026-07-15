"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Categories Schema

Purpose :
    Stores vault categories.
===============================================================
"""

from __future__ import annotations

TABLE_NAME = "Categories"

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

CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME}
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    category_name TEXT NOT NULL UNIQUE
);
"""

CREATE_INDEXES = [

f"""
CREATE UNIQUE INDEX IF NOT EXISTS
idx_categories_name
ON {TABLE_NAME}(category_name);
"""

]