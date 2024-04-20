from contextlib import contextmanager
from logging import LogRecord, getLogger, handlers
from multiprocessing import Queue

import pytest


@pytest.fixture()
def caplog_workaround():
    """Workaround for caplog fixture not capturing logs from other processes."""

    @contextmanager
    def ctx():
        """Context manager to capture logs from other processes."""
        logger_queue = Queue()
        logger = getLogger()
        logger.addHandler(handlers.QueueHandler(logger_queue))
        yield
        while not logger_queue.empty():
            log_record: LogRecord = logger_queue.get()
            logger._log(  # pylint: disable=protected-access
                level=log_record.levelno,
                msg=log_record.message,
                args=log_record.args,
                exc_info=log_record.exc_info,
            )

    return ctx
