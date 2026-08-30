import logging
from logging.handlers import RotatingFileHandler

from utils.logger import get_logger


def test_logger_is_configured():
    logger = get_logger("test.logging")
    assert logger.level == logging.INFO
    assert logger.handlers


def test_logger_does_not_duplicate_handlers():
    first = get_logger("test.no_duplicates")
    count = len(first.handlers)
    second = get_logger("test.no_duplicates")
    assert first is second
    assert len(second.handlers) == count


def test_logger_has_rotating_file_handler():
    logger = get_logger("test.rotating")
    assert any(
        isinstance(handler, RotatingFileHandler)
        for handler in logger.handlers
    )
