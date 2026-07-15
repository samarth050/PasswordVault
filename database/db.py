"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Database Manager

Purpose :
    Enterprise SQLite database manager.

===============================================================
"""

from __future__ import annotations

import sqlite3

from pathlib import Path

from typing import Any
from typing import Iterable

from database.version import (
    DATABASE_VERSION,
)

from database.schema import (
    ALL_TABLES,
    ALL_INDEXES,
)

from database.seed import DatabaseSeeder

from database.migration import DatabaseMigration

from utils.constants import DATABASE_FILE

from utils.logger import Logger


class DatabaseManager:
    """
    Enterprise SQLite database manager.

    Responsibilities
    ----------------

    • Open database

    • Create schema

    • Create indexes

    • Seed default data

    • Execute migrations

    • Execute SQL

    • Manage transactions

    • Close database safely
    """

    def __init__(self) -> None:

        self.logger = Logger.get_logger()

        self.db_path: Path = DATABASE_FILE

        self.connection: sqlite3.Connection | None = None

        self.cursor: sqlite3.Cursor | None = None

    # ---------------------------------------------------------

    def connect(self) -> None:
        """
        Opens the SQLite database.
        """

        if self.connection is not None:
            return

        self.logger.info(
            "Opening database %s",
            self.db_path
        )

        self.connection = sqlite3.connect(
            self.db_path
        )

        self.connection.row_factory = sqlite3.Row

        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        self.cursor = self.connection.cursor()

    # ---------------------------------------------------------

    def close(self) -> None:
        """
        Closes the database.
        """

        if self.connection is None:
            return

        self.logger.info(
            "Closing database."
        )

        self.connection.close()

        self.connection = None

        self.cursor = None

    # ---------------------------------------------------------

    def __enter__(self) -> "DatabaseManager":

        self.connect()

        return self

    # ---------------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ) -> None:

        if self.connection is not None:

            if exc_type is None:

                self.connection.commit()

                self.logger.info(
                    "Transaction committed."
                )

            else:

                self.connection.rollback()

                self.logger.exception(
                    "Transaction rolled back."
                )

        self.close()

    # ---------------------------------------------------------

    def execute(
        self,
        sql: str,
        parameters: tuple[Any, ...] = ()
    ) -> sqlite3.Cursor:
        """
        Execute one SQL statement.
        """

        if self.cursor is None:
            raise RuntimeError(
                "Database not connected."
            )

        self.logger.debug(sql)

        return self.cursor.execute(
            sql,
            parameters
        )

    # ---------------------------------------------------------

    def executemany(
        self,
        sql: str,
        parameters: Iterable[
            tuple[Any, ...]
        ]
    ) -> sqlite3.Cursor:
        """
        Execute multiple SQL statements.
        """

        if self.cursor is None:
            raise RuntimeError(
                "Database not connected."
            )

        self.logger.debug(
            "executemany()"
        )

        return self.cursor.executemany(
            sql,
            parameters
        )

    # ---------------------------------------------------------

    def fetch_one(
        self,
        sql: str,
        parameters: tuple[Any, ...] = ()
    ) -> sqlite3.Row | None:
        """
        Returns one row.
        """

        cursor = self.execute(
            sql,
            parameters
        )

        return cursor.fetchone()

    # ---------------------------------------------------------

    def fetch_all(
        self,
        sql: str,
        parameters: tuple[Any, ...] = ()
    ) -> list[sqlite3.Row]:
        """
        Returns all rows.
        """

        cursor = self.execute(
            sql,
            parameters
        )

        return cursor.fetchall()

    # ---------------------------------------------------------

    def create_tables(self) -> None:
        """
        Creates all database tables.
        """

        self.logger.info(
            "Creating database tables."
        )

        for sql in ALL_TABLES:

            self.cursor.execute(sql)

    # ---------------------------------------------------------

    def create_indexes(self) -> None:
        """
        Creates all database indexes.
        """

        self.logger.info(
            "Creating database indexes."
        )

        for sql in ALL_INDEXES:

            self.cursor.execute(sql)

    # ---------------------------------------------------------

    def database_exists(self) -> bool:
        """
        Returns True if the database file exists.
        """

        return self.db_path.exists()

    # ---------------------------------------------------------

    def table_exists(
        self,
        table_name: str
    ) -> bool:
        """
        Returns True if the specified table exists.
        """

        row = self.fetch_one(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?
            """,
            (
                table_name,
            ),
        )

        return row is not None

    # ---------------------------------------------------------

    def index_exists(
        self,
        index_name: str
    ) -> bool:
        """
        Returns True if the specified index exists.
        """

        row = self.fetch_one(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='index'
            AND name=?
            """,
            (
                index_name,
            ),
        )

        return row is not None

    # ---------------------------------------------------------

    def get_table_count(self) -> int:
        """
        Returns the number of user tables.
        """

        row = self.fetch_one(
            """
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            """
        )

        return int(row[0])

    # ---------------------------------------------------------

    def get_index_count(self) -> int:
        """
        Returns the number of indexes.
        """

        row = self.fetch_one(
            """
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type='index'
            AND name NOT LIKE 'sqlite_%'
            """
        )

        return int(row[0])

    # ---------------------------------------------------------

    def database_information(self) -> dict[str, Any]:
        """
        Returns basic database information.
        """

        return {

            "database_exists": self.database_exists(),

            "tables": self.get_table_count(),

            "indexes": self.get_index_count(),

            "database_version": DATABASE_VERSION,

        }

    # ---------------------------------------------------------

    def initialize_database(self) -> None:
        """
        Initializes the database.

        This method is safe to call every time the
        application starts.
        """

        self.logger.info(
            "Initializing database."
        )

        self.connect()

        self.create_tables()

        self.create_indexes()

        self.run_migrations()

        self.seed_database()

        self.connection.commit()

        self.logger.info(
            "Database initialization completed."
        )

    # ---------------------------------------------------------

    def seed_database(self) -> None:
        """
        Inserts default data into the database.
        """

        self.logger.info(
            "Running database seed."
        )

        DatabaseSeeder(
            self.connection
        ).seed_all()

    # ---------------------------------------------------------

    def run_migrations(self) -> None:
        """
        Executes pending database migrations.
        """

        self.logger.info(
            "Checking database migrations."
        )

        migration = DatabaseMigration(
            self.connection
        )

        if migration.migration_required():

            self.logger.info(
                "Database migration required."
            )

            migration.migrate()

        else:

            self.logger.info(
                "Database already up to date."
            )

    # ---------------------------------------------------------

    def get_database_version(self) -> int:
        """
        Returns the database version stored
        in the DatabaseInfo table.
        """

        row = self.fetch_one(
            """
            SELECT database_version
            FROM DatabaseInfo
            WHERE id = 1
            """
        )

        if row is None:

            return 0

        return int(row["database_version"])

    # ---------------------------------------------------------

    def is_initialized(self) -> bool:
        """
        Returns True if DatabaseInfo exists
        and contains the initialization record.
        """

        if not self.table_exists(
            "DatabaseInfo"
        ):

            return False

        row = self.fetch_one(
            """
            SELECT COUNT(*)
            FROM DatabaseInfo
            """
        )

        return row[0] > 0

    # ---------------------------------------------------------

    def get_categories(self) -> list[str]:
        """
        Returns all category names.
        """

        rows = self.fetch_all(
            """
            SELECT category_name
            FROM Categories
            ORDER BY category_name
            """
        )

        return [
            row["category_name"]
            for row in rows
        ]

    # ---------------------------------------------------------

    def get_application_settings(
        self
    ) -> dict[str, str]:
        """
        Returns all application settings.
        """

        rows = self.fetch_all(
            """
            SELECT
                setting_name,
                setting_value
            FROM ApplicationSettings
            """
        )

        settings: dict[str, str] = {}

        for row in rows:

            settings[
                row["setting_name"]
            ] = row["setting_value"]

        return settings

    # ---------------------------------------------------------

    def health_check(self) -> bool:
        """
        Performs a simple database health check.
        """

        try:

            self.fetch_one(
                "SELECT 1"
            )

            return True

        except sqlite3.Error:

            return False

    # ---------------------------------------------------------

    def commit(self) -> None:
        """
        Commits the current transaction.
        """

        if self.connection is None:
            return

        self.connection.commit()

        self.logger.info(
            "Transaction committed."
        )

    # ---------------------------------------------------------

    def rollback(self) -> None:
        """
        Rolls back the current transaction.
        """

        if self.connection is None:
            return

        self.connection.rollback()

        self.logger.warning(
            "Transaction rolled back."
        )

    # ---------------------------------------------------------

    @property
    def last_row_id(self) -> int:
        """
        Returns the last inserted row id.
        """

        if self.cursor is None:
            return 0

        return self.cursor.lastrowid

    # ---------------------------------------------------------

    @property
    def row_count(self) -> int:
        """
        Returns the number of affected rows.
        """

        if self.cursor is None:
            return 0

        return self.cursor.rowcount

    # ---------------------------------------------------------

    def integrity_check(self) -> bool:
        """
        Executes SQLite integrity check.

        Returns
        -------
        bool
            True if database integrity is OK.
        """

        row = self.fetch_one(
            "PRAGMA integrity_check"
        )

        if row is None:
            return False

        return row[0].lower() == "ok"

    # ---------------------------------------------------------

    def optimize(self) -> None:
        """
        Updates SQLite query statistics.
        """

        self.logger.info(
            "Running ANALYZE."
        )

        self.execute(
            "ANALYZE"
        )

        self.commit()

    # ---------------------------------------------------------

    def vacuum(self) -> None:
        """
        Rebuilds the database file and
        recovers unused space.
        """

        self.logger.info(
            "Running VACUUM."
        )

        #
        # VACUUM cannot execute inside
        # an active transaction.
        #

        self.commit()

        self.connection.execute(
            "VACUUM"
        )

    # ---------------------------------------------------------

    def begin_transaction(self) -> None:
        """
        Starts an explicit transaction.
        """

        self.execute(
            "BEGIN"
        )

    # ---------------------------------------------------------

    def execute_script(
        self,
        script: str
    ) -> None:
        """
        Executes a SQL script.
        """

        if self.cursor is None:
            raise RuntimeError(
                "Database not connected."
            )

        self.cursor.executescript(
            script
        )

    # ---------------------------------------------------------

    def database_size(self) -> int:
        """
        Returns database size in bytes.
        """

        if not self.database_exists():
            return 0

        return self.db_path.stat().st_size

    # ---------------------------------------------------------

    def __repr__(self) -> str:
        """
        Returns string representation.
        """

        return (
            f"DatabaseManager("
            f"path='{self.db_path}')"
        )                