"""
Password Vault

Phase 2
"""

from database.db import DatabaseManager


def main():

    print()

    print("---------------------------------------")
    print(" Password Vault")
    print("---------------------------------------")

    db = DatabaseManager()

    db.create_database()

    print("Database initialized successfully.")

    print()


if __name__ == "__main__":

    main()