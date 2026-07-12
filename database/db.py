"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Database Manager
Purpose : SQLite database connection manager.

===============================================================
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from utils.constants import DATABASE_FILE
from utils.logger import Logger


class DatabaseManager:
    """
    Enterprise SQLite database manager.

    Features
    --------
    * Context manager support
    * Automatic transactions
    * Foreign key enforcement
    * Logging
    * Future migration support
    """

    def __init__(self) -> None:

        self._connection: Optional[sqlite3.Connection] = None
        self._cursor: Optional[sqlite3.Cursor] = None

        self.logger = Logger.get_logger()

    # ----------------------------------------------------------

    def connect(self) -> None:
        """
        Opens a database connection.
        """

        if self._connection is not None:
            return

        self.logger.info("Opening database connection.")

        self._connection = sqlite3.connect(DATABASE_FILE)

        self._connection.row_factory = sqlite3.Row

        self._connection.execute("PRAGMA foreign_keys = ON")

        self._cursor = self._connection.cursor()

    # ----------------------------------------------------------

    def close(self) -> None:
        """
        Closes the database connection.
        """

        if self._connection is None:
            return

        self.logger.info("Closing database connection.")

        self._connection.close()

        self._connection = None

        self._cursor = None

    # ----------------------------------------------------------

    @property
    def connection(self) -> sqlite3.Connection:
        """
        Returns the active SQLite connection.
        """

        if self._connection is None:
            self.connect()

        return self._connection

    # ----------------------------------------------------------

    @property
    def cursor(self) -> sqlite3.Cursor:
        """
        Returns the active cursor.
        """

        if self._cursor is None:
            self.connect()

        return self._cursor

    # ----------------------------------------------------------

    # ----------------------------------------------------------
    # Generic Database Operations
    # ----------------------------------------------------------

    def execute(
        self,
        sql: str,
        parameters: tuple = ()
    ) -> sqlite3.Cursor:
        """
        Execute a single SQL statement.

        Parameters
        ----------
        sql : str
            SQL statement.

        parameters : tuple
            SQL parameters.

        Returns
        -------
        sqlite3.Cursor
        """

        self.logger.debug("Executing SQL:\n%s", sql)

        try:

            cursor = self.cursor.execute(sql, parameters)

            return cursor

        except sqlite3.Error as ex:

            self.logger.exception(
                "Database execute() failed."
            )

            raise ex

    # ----------------------------------------------------------

    def executemany(
        self,
        sql: str,
        parameter_list: list[tuple]
    ) -> sqlite3.Cursor:
        """
        Execute multiple SQL statements.
        """

        self.logger.debug(
            "Executing executemany()."
        )

        try:

            cursor = self.cursor.executemany(
                sql,
                parameter_list
            )

            return cursor

        except sqlite3.Error as ex:

            self.logger.exception(
                "Database executemany() failed."
            )

            raise ex

    # ----------------------------------------------------------

    def fetch_one(
        self,
        sql: str,
        parameters: tuple = ()
    ) -> sqlite3.Row | None:
        """
        Returns one row.
        """

        cursor = self.execute(sql, parameters)

        return cursor.fetchone()

    # ----------------------------------------------------------

    def fetch_all(
        self,
        sql: str,
        parameters: tuple = ()
    ) -> list[sqlite3.Row]:
        """
        Returns all rows.
        """

        cursor = self.execute(sql, parameters)

        return cursor.fetchall()

    # ----------------------------------------------------------

    def commit(self) -> None:
        """
        Commits current transaction.
        """

        if self._connection:

            self._connection.commit()

            self.logger.info(
                "Database commit completed."
            )

    # ----------------------------------------------------------

    def rollback(self) -> None:
        """
        Rolls back current transaction.
        """

        if self._connection:

            self._connection.rollback()

            self.logger.warning(
                "Database rollback executed."
            )

    # ----------------------------------------------------------

    def last_row_id(self) -> int:
        """
        Returns last inserted row id.
        """

        return self.cursor.lastrowid

    # ----------------------------------------------------------

    def row_count(self) -> int:
        """
        Returns affected row count.
        """

        return self.cursor.rowcount

    # ----------------------------------------------------------

    def table_exists(
        self,
        table_name: str
    ) -> bool:
        """
        Checks whether a table exists.
        """

        row = self.fetch_one(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name=?
            """,
            (table_name,)
        )

        return row is not None


    def __enter__(self) -> "DatabaseManager":
        """
        Context manager entry.
        """

        self.connect()

        return self

    # ----------------------------------------------------------

    def __exit__(self,
                 exc_type,
                 exc_value,
                 traceback) -> None:
        """
        Context manager exit.
        """

        if self._connection:

            if exc_type is None:

                self._connection.commit()

                self.logger.info("Transaction committed.")

            else:

                self._connection.rollback()

                self.logger.error(
                    "Transaction rolled back."
                )

        self.close()