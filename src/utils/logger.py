"""A simple wrapper around the logging module."""
import logging
import logging.config
import sys


class Logger:
    """A simple wrapper around the logging module.

    This class is a simple wrapper around the logging module. It allows for
    easy configuration of the logging module and provides a simple interface
    for logging messages.

    :param name: The name of the logger to use
    :type name: str
    :param config_path: The path to the logging configuration file
    :type config_path: str
    """

    _logger = None
    config_path = None

    def __init__(self, name="custom", config_path=None):
        """Initialize the Logger class."""

        # Set a default path or use another method to find the config file
        # config_path = os.path.join(os.path.dirname(__file__), "../logging.conf")
        self.config_path = config_path or "logging.conf"

        try:
            logging.config.fileConfig(self.config_path)
            self._logger = logging.getLogger(name)
        except Exception as e:  # pylint: disable=broad-except
            # Handle exceptions, perhaps default to basicConfig if file not found
            logging.basicConfig(
                level=logging.INFO,
                format="%(levelname)s - %(message)s",
                handlers=[logging.StreamHandler(stream=sys.stdout)],
            )
            self._logger = logging.getLogger(name)
            self._logger.error("Failed to load logging configuration: %s", e)

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
