"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Cryptography

Purpose :
    Encryption and decryption services.

===============================================================
"""

from __future__ import annotations

import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import (
    PBKDF2HMAC,
)

from utils.constants import (
    KEY_LENGTH,
    PBKDF2_ITERATIONS,
    SALT_LENGTH,
)


class CryptoManager:
    """
    Provides encryption and decryption services
    using a key derived from the master password.
    """

    @staticmethod
    def generate_salt() -> bytes:
        """
        Generates a cryptographically secure salt.
        """

        return os.urandom(SALT_LENGTH)

    # ---------------------------------------------------------

    @staticmethod
    def derive_key(
        master_password: str,
        salt: bytes,
    ) -> bytes:
        """
        Derives a Fernet-compatible encryption key.
        """

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_LENGTH,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
        )

        key = kdf.derive(
            master_password.encode("utf-8")
        )

        return base64.urlsafe_b64encode(key)

    # ---------------------------------------------------------

    @staticmethod
    def encrypt(
        plaintext: str,
        key: bytes,
    ) -> str:
        """
        Encrypts text.
        """

        fernet = Fernet(key)

        token = fernet.encrypt(
            plaintext.encode("utf-8")
        )

        return token.decode("utf-8")

    # ---------------------------------------------------------

    @staticmethod
    def decrypt(
        ciphertext: str,
        key: bytes,
    ) -> str:
        """
        Decrypts text.
        """

        fernet = Fernet(key)

        plaintext = fernet.decrypt(
            ciphertext.encode("utf-8")
        )

        return plaintext.decode("utf-8")