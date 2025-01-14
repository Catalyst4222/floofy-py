import logging
import os
import time
from typing import Optional

FORMATTER = logging.Formatter("%(asctime)s UTC || %(levelname)s || %(message)s")
FORMATTER.converter = time.gmtime


def get_base_logger(name: str | None = "floofy") -> logging.Logger:
    """
    Sets up the overall loggin on the bot.

    Any logging in extensions should use :py:func:`logging.getLogger` and pass ``"{name}.{ext}"``
    (e.x. the logger in :py:mod:`extensions.utility` would use ``logging.getLogger("floofy.utility")`` for its logger)
    """
    log = logging.getLogger(name=name)
    log.setLevel(logging.DEBUG)

    # log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(FORMATTER)

    # log to file
    file_handler = logging.FileHandler(
        filename=f"./{name}.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(FORMATTER)

    level = os.getenv("LOG_LEVEL", "INFO")
    console_handler.setLevel(level)
    file_handler.setLevel(level)

    log.addHandler(console_handler)
    log.addHandler(file_handler)

    return log
