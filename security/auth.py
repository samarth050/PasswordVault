"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Authentication

Purpose :
    Master password hashing and verification.

===============================================================
"""

from __future__ import annotations

import base64
import hashlib
import hmac

from security.crypto import CryptoManager


class AuthenticationManager:
    """
    Handles master password hashing and verification.
    """

    HASH_NAME = "sha256"

    # ---------------------------------------------------------

    @staticmethod
    def create_password_credentials(
        master_password: str,
    ) -> tuple[str, str]:
        """
        Creates a password hash and salt for storage.

        Returns
        -------
        tuple
            (password_hash, salt_base64)
        """

        salt = CryptoManager.generate_salt()

        password_hash = hashlib.pbkdf2_hmac(
            AuthenticationManager.HASH_NAME,
            master_password.encode("utf-8"),
            salt,
            200_000,
        )

        return (
            base64.b64encode(password_hash).decode("utf-8"),
            base64.b64encode(salt).decode("utf-8"),
        )

    # ---------------------------------------------------------

    @staticmethod
    def verify_password(
        master_password: str,
        stored_hash: str,
        stored_salt: str,
    ) -> bool:
        """
        Verifies the supplied master password.

        Returns
        -------
        bool
        """

        salt = base64.b64decode(stored_salt)

        calculated_hash = hashlib.pbkdf2_hmac(
            AuthenticationManager.HASH_NAME,
            master_password.encode("utf-8"),
            salt,
            200_000,
        )

        calculated_hash_b64 = base64.b64encode(
            calculated_hash
        ).decode("utf-8")

        return hmac.compare_digest(
            calculated_hash_b64,
            stored_hash,
        )

    # ---------------------------------------------------------

    @staticmethod
    def get_encryption_key(
        master_password: str,
        stored_salt: str,
    ) -> bytes:
        """
        Derives the Fernet encryption key from the
        master password and stored salt.
        """

        salt = base64.b64decode(stored_salt)

        return CryptoManager.derive_key(
            master_password,
            salt,
        )