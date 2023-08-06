#!/usr/bin/env python
import logging
from logging import Logger


def init_logger(module_name: str) -> Logger:
    logger: Logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    console_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    logger.addHandler(console_handler)

    return logger
