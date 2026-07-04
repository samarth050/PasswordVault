"""
Database Backup Utilities
"""

import shutil
from pathlib import Path
from datetime import datetime

from database.schema import DATABASE_NAME


class DatabaseBackup:

    @staticmethod
    def create_backup():

        source = Path(DATABASE_NAME)

        if not source.exists():
            return None

        backup_folder = Path("Backups")

        backup_folder.mkdir(exist_ok=True)

        filename = datetime.now().strftime(
            "Vault_%Y%m%d_%H%M%S.db"
        )

        destination = backup_folder / filename

        shutil.copy2(source, destination)

        return destination