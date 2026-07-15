"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Database Migration

Purpose :
    Handles database schema version upgrades.

===============================================================
"""

from __future__ import annotations

import sqlite3

from database.version import DATABASE_VERSION


class DatabaseMigration:
    """
    Handles database schema migrations.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.cursor = connection.cursor()

    # ----------------------------------------------------------

    def get_database_version(self) -> int:
        """
        Returns the current database version.

        Returns
        -------
        int
            Database version stored in DatabaseInfo.
            Returns 0 if the table or record does not exist.
        """

        try:

            self.cursor.execute(
                """
                SELECT database_version
                FROM DatabaseInfo
                WHERE id = 1
                """
            )

            row = self.cursor.fetchone()

            if row is None:
                return 0

            return int(row[0])

        except sqlite3.Error:
            return 0

    # ----------------------------------------------------------

    def migration_required(self) -> bool:
        """
        Returns True if the database requires migration.
        """

        return self.get_database_version() < DATABASE_VERSION

    # ----------------------------------------------------------

    def migrate(self) -> None:
        """
        Executes required database migrations.

        Version 1 has no migrations because it is the
        initial database release.
        """

        current_version = self.get_database_version()

        if current_version == 0:
            return

        if current_version >= DATABASE_VERSION:
            return

        #
        # Future example:
        #
        # if current_version < 2:
        #     self._migrate_v2()
        #
        # if current_version < 3:
        #     self._migrate_v3()
        #

        self.cursor.execute(
            """
            UPDATE DatabaseInfo
            SET database_version = ?
            WHERE id = 1
            """,
            (DATABASE_VERSION,),
        )

        self.connection.commit()