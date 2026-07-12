"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Database Schema Package

Purpose :
    Exposes all schema definitions for database creation.

===============================================================
"""

from .database_info import CREATE_DATABASE_INFO_TABLE
from .users import CREATE_USERS_TABLE
from .vaults import CREATE_VAULTS_TABLE
from .categories import (
    CREATE_CATEGORIES_TABLE,
    DEFAULT_CATEGORIES,
)
from .vault_items import CREATE_VAULT_ITEMS_TABLE
from .password_history import CREATE_PASSWORD_HISTORY_TABLE
from .audit_log import CREATE_AUDIT_LOG_TABLE
from .application_settings import (
    CREATE_APPLICATION_SETTINGS_TABLE,
    DEFAULT_APPLICATION_SETTINGS,
)

ALL_TABLES = (
    CREATE_DATABASE_INFO_TABLE,
    CREATE_USERS_TABLE,
    CREATE_VAULTS_TABLE,
    CREATE_CATEGORIES_TABLE,
    CREATE_VAULT_ITEMS_TABLE,
    CREATE_PASSWORD_HISTORY_TABLE,
    CREATE_AUDIT_LOG_TABLE,
    CREATE_APPLICATION_SETTINGS_TABLE,
)