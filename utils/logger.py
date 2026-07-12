"""
===============================================================
VaultX Enterprise
---------------------------------------------------------------
Author  : Samarth Sinha
Version : 0.1.0

Module  : Logger
Purpose : Centralized application logging.
===============================================================
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from utils.constants import (
    APP_NAME,
    LOG_DIR,
    LOG_FILE_NAME,
    LOG_LEVEL,
)


class Logger:
    """
    Centralized logging utility.
    """

    _logger: logging.Logger | None = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Returns the singleton logger instance.
        """

        if cls._logger is not None:
            return cls._logger

        LOG_DIR.mkdir(exist_ok=True)

        log_file: Path = LOG_DIR / LOG_FILE_NAME

        logger = logging.getLogger(APP_NAME)

        logger.setLevel(getattr(logging, LOG_LEVEL))

        if not logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(message)s"
            )

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=1_000_000,
                backupCount=5,
                encoding="utf-8",
            )

            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()

            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        cls._logger = logger

        return logger