from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import (
    LOG_BACKUP_COUNT,
    LOG_LEVEL,
    LOG_MAX_BYTES,
)


LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_FILE = LOG_DIR / "app.log"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(name)s | %(message)s"
)


def get_logger(name: str) -> logging.Logger:
    """
    Return a rotating project logger.

    Secrets are never added to the logging configuration.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    level = getattr(
        logging,
        LOG_LEVEL,
        logging.INFO,
    )

    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        LOG_FORMAT
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
