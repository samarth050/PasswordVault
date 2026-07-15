"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Schema Package

Purpose :
    Imports all database schema definitions.
===============================================================
"""

from .database_info import (
    CREATE_TABLE as DATABASE_INFO_TABLE,
    CREATE_INDEXES as DATABASE_INFO_INDEXES,
)

from .users import (
    CREATE_TABLE as USERS_TABLE,
    CREATE_INDEXES as USERS_INDEXES,
)

from .vaults import (
    CREATE_TABLE as VAULTS_TABLE,
    CREATE_INDEXES as VAULTS_INDEXES,
)

from .categories import (
    CREATE_TABLE as CATEGORIES_TABLE,
    CREATE_INDEXES as CATEGORIES_INDEXES,
    DEFAULT_CATEGORIES,
)

from .vault_items import (
    CREATE_TABLE as VAULT_ITEMS_TABLE,
    CREATE_INDEXES as VAULT_ITEMS_INDEXES,
)

from .password_history import (
    CREATE_TABLE as PASSWORD_HISTORY_TABLE,
    CREATE_INDEXES as PASSWORD_HISTORY_INDEXES,
)

from .audit_log import (
    CREATE_TABLE as AUDIT_LOG_TABLE,
    CREATE_INDEXES as AUDIT_LOG_INDEXES,
)

from .application_settings import (
    CREATE_TABLE as APPLICATION_SETTINGS_TABLE,
    CREATE_INDEXES as APPLICATION_SETTINGS_INDEXES,
    DEFAULT_APPLICATION_SETTINGS,
)

ALL_TABLES = [

    DATABASE_INFO_TABLE,

    USERS_TABLE,

    VAULTS_TABLE,

    CATEGORIES_TABLE,

    VAULT_ITEMS_TABLE,

    PASSWORD_HISTORY_TABLE,

    AUDIT_LOG_TABLE,

    APPLICATION_SETTINGS_TABLE

]

ALL_INDEXES = (

    DATABASE_INFO_INDEXES +

    USERS_INDEXES +

    VAULTS_INDEXES +

    CATEGORIES_INDEXES +

    VAULT_ITEMS_INDEXES +

    PASSWORD_HISTORY_INDEXES +

    AUDIT_LOG_INDEXES +

    APPLICATION_SETTINGS_INDEXES

)