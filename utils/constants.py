"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Module  : Application Constants
Purpose : Global constants used throughout the application.
===============================================================
"""

from pathlib import Path

# ===============================================================
# Application Information
# ===============================================================

APP_NAME: str = "VaultX Enterprise"
APP_VERSION: str = "0.1.0"

# ===============================================================
# Directory Structure
# ===============================================================

ROOT_DIR: Path = Path(__file__).resolve().parent.parent

DATABASE_DIR: Path = ROOT_DIR
DATABASE_FILE: Path = DATABASE_DIR / "vault.db"

BACKUP_DIR: Path = ROOT_DIR / "Backups"
LOG_DIR: Path = ROOT_DIR / "Logs"
RESOURCE_DIR: Path = ROOT_DIR / "resources"
ICON_DIR: Path = RESOURCE_DIR / "icons"
THEME_DIR: Path = RESOURCE_DIR / "themes"

# ===============================================================
# Security
# ===============================================================

PBKDF2_ITERATIONS: int = 200_000
KEY_LENGTH: int = 32
SALT_LENGTH: int = 16

# ===============================================================
# Session
# ===============================================================

DEFAULT_AUTO_LOCK_MINUTES: int = 5
DEFAULT_CLIPBOARD_TIMEOUT: int = 20

# ===============================================================
# Database
# ===============================================================

DATABASE_VERSION: int = 1
ENCRYPTION_VERSION: int = 1

# ===============================================================
# Logging
# ===============================================================

LOG_FILE_NAME: str = "vault.log"
LOG_LEVEL: str = "INFO"