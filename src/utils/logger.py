import logging
import logging.config
import sys
import os

class Logger:
    def __init__(self, name="custom"):
        config_path = "logging.ini"
        if os.path.exists(config_path):
            try:
                logging.config.fileConfig(config_path)
            except KeyError as e:
                logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
                logging.getLogger(name).error("Failed to load logging configuration: %s", e)
        else:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        self._logger = logging.getLogger(name)

    def info(self, message, *args):
        """Log an info message."""
        self._logger.info(message, *args)

    def error(self, message, *args):
        """Log an error message."""
        self._logger.error(message, *args)

    def debug(self, message, *args):
        """Log a debug message."""
        self._logger.debug(message, *args)

    def warning(self, message, *args):
        """Log a warning message."""
        self._logger.warning(message, *args)

    def critical(self, message, *args):
        """Log a critical message."""
        self._logger.critical(message, *args)

    def exception(self, message, *args):
        """Log an exception message."""
        self._logger.exception(message, *args)
