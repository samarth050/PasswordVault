"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Database Seed

Purpose :
    Inserts default data into the database.

===============================================================
"""

from __future__ import annotations

from datetime import datetime
import sqlite3

from database.version import (
    DATABASE_VERSION,
    ENCRYPTION_VERSION,
    APPLICATION_VERSION,
)

from database.schema import (
    DEFAULT_CATEGORIES,
    DEFAULT_APPLICATION_SETTINGS,
)


class DatabaseSeeder:
    """
    Seeds the database with initial data.

    All methods are idempotent. Running them multiple
    times will not create duplicate records.
    """

    def __init__(
        self,
        connection: sqlite3.Connection
    ) -> None:

        self.connection = connection
        self.cursor = connection.cursor()

    # ----------------------------------------------------------

    def seed_all(self) -> None:
        """
        Executes all seed operations.
        """

        self.seed_database_info()
        self.seed_categories()
        self.seed_application_settings()

    # ----------------------------------------------------------

    def seed_database_info(self) -> None:
        """
        Inserts the initial DatabaseInfo record.
        """

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM DatabaseInfo
            """
        )

        count = self.cursor.fetchone()[0]

        if count > 0:
            return

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        self.cursor.execute(
            """
            INSERT INTO DatabaseInfo
            (
                id,
                database_version,
                encryption_version,
                application_version,
                created_on,
                last_upgrade
            )
            VALUES
            (?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                DATABASE_VERSION,
                ENCRYPTION_VERSION,
                APPLICATION_VERSION,
                now,
                now,
            ),
        )

    # ----------------------------------------------------------

    def seed_categories(self) -> None:
        """
        Inserts default categories.
        """

        for category in DEFAULT_CATEGORIES:

            self.cursor.execute(
                """
                INSERT OR IGNORE INTO Categories
                (
                    category_name
                )
                VALUES
                (?)
                """,
                (category,),
            )

    # ----------------------------------------------------------

    def seed_application_settings(self) -> None:
        """
        Inserts default application settings.
        """

        for name, value in DEFAULT_APPLICATION_SETTINGS.items():

            self.cursor.execute(
                """
                INSERT OR IGNORE INTO ApplicationSettings
                (
                    setting_name,
                    setting_value
                )
                VALUES
                (?, ?)
                """,
                (
                    name,
                    value,
                ),
            )