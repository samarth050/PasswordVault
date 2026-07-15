"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Authentication Service

Purpose :
    Handles first-run setup and user authentication.

===============================================================
"""

from __future__ import annotations

from security.auth import AuthenticationManager
from database.db import DatabaseManager


class AuthService:
    """
    Authentication service.
    """

    # ---------------------------------------------------------

    def is_first_run(self) -> bool:
        """
        Returns True if no users exist.
        """

        with DatabaseManager() as db:

            db.initialize_database()

            row = db.fetch_one(
                """
                SELECT COUNT(*)
                AS total
                FROM Users
                """
            )

            return row["total"] == 0

    # ---------------------------------------------------------

    def create_admin_user(
        self,
        username: str,
        master_password: str,
        display_name: str = "Administrator",
        email: str = "",
    ) -> bool:
        """
        Creates the initial administrator account.

        Returns
        -------
        bool
            True if created successfully.
        """

        password_hash, salt = (
            AuthenticationManager.create_password_credentials(
                master_password
            )
        )

        with DatabaseManager() as db:

            db.initialize_database()

            existing = db.fetch_one(
                """
                SELECT id
                FROM Users
                WHERE username = ?
                """,
                (username,),
            )

            if existing is not None:
                return False

            db.execute(
                """
                INSERT INTO Users
                (
                    username,
                    password_hash,
                    salt,
                    display_name,
                    email,
                    created_on,
                    active
                )
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    datetime('now'),
                    1
                )
                """,
                (
                    username,
                    password_hash,
                    salt,
                    display_name,
                    email,
                ),
            )

    
        return True

    # ---------------------------------------------------------

    def authenticate(
        self,
        username: str,
        master_password: str,
    ) -> tuple[bool, bytes | None]:
        """
        Authenticates a user.

        Returns
        -------
        tuple
            (success, encryption_key)
        """

        with DatabaseManager() as db:

            db.initialize_database()

            row = db.fetch_one(
                """
                SELECT
                    password_hash,
                    salt
                FROM Users
                WHERE username = ?
                AND active = 1
                """,
                (username,),
            )

            if row is None:
                return False, None

            if not AuthenticationManager.verify_password(
                master_password,
                row["password_hash"],
                row["salt"],
            ):
                return False, None

            key = AuthenticationManager.get_encryption_key(
                master_password,
                row["salt"],
            )

            db.execute(
                """
                UPDATE Users
                SET last_login = datetime('now')
                WHERE username = ?
                """,
                (username,),
            )


            return True, key