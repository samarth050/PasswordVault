"""
Database Manager
"""

import sqlite3

from pathlib import Path

from database.schema import *


class DatabaseManager:

    def __init__(self):

        self.db_path = Path(DATABASE_NAME)

        self.connection = None

        self.cursor = None

    def connect(self):

        self.connection = sqlite3.connect(self.db_path)

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

    def close(self):

        if self.connection:

            self.connection.close()

    def create_database(self):

        self.connect()

        self.cursor.execute(CREATE_SETTINGS_TABLE)

        self.cursor.execute(CREATE_VAULT_TABLE)

        self.cursor.execute(CREATE_INDEX1)

        self.cursor.execute(CREATE_INDEX2)

        self.connection.commit()

        self.close()

    def execute(self, sql, params=()):

        self.connect()

        self.cursor.execute(sql, params)

        self.connection.commit()

        self.close()

    def fetchone(self, sql, params=()):

        self.connect()

        self.cursor.execute(sql, params)

        row = self.cursor.fetchone()

        self.close()

        return row

    def fetchall(self, sql, params=()):

        self.connect()

        self.cursor.execute(sql, params)

        rows = self.cursor.fetchall()

        self.close()

        return rows