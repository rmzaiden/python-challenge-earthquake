"""This is the main module of the project."""

from utils import Logger

logger = Logger(name="main")


def hello():
    """Prints "Hello World!" to stdout

    :return: None
    """
    logger.info("Hello World!")


if __name__ == "__main__":  # pragma: no cover
    hello()
