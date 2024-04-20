import pytest

from src.utils.logger import Logger


def test_info_log(capsys):
    logger = Logger(name="custom")
    logger.info("Test Info", {"test": "test"})

    assert "INFO - Test Info - {'test': 'test'}\n" in capsys.readouterr().out


def test_error_log(capsys):
    logger = Logger(name="custom")
    logger.error("Test Error", {"test": "test"})

    assert "ERROR - Test Error - {'test': 'test'}\n" in capsys.readouterr().out


def test_debug_log(capsys):
    logger = Logger(name="custom")
    logger.debug("Test Debug", {"test": "test"})

    assert "DEBUG - Test Debug - {'test': 'test'}" in capsys.readouterr().out


def test_warning_log(capsys):
    logger = Logger(name="custom")
    logger.warning("Test Warning", {"test": "test"})

    assert "WARNING - Test Warning - {'test': 'test'}\n" in capsys.readouterr().out


def test_critical_log(capsys):
    logger = Logger(name="custom")
    logger.critical("Test Critical", {"test": "test"})

    assert "CRITICAL - Test Critical - {'test': 'test'}\n" in capsys.readouterr().out


def test_exception_log(capsys):
    logger = Logger(name="custom")
    try:
        raise ValueError("Test Exception")
    except ValueError as e:
        logger.exception("Test Exception", {"test": "test"})
        content = capsys.readouterr().out

        assert "ERROR - Test Exception" in content
        assert str(e) in content


def test_default_config_path():
    logger = Logger(name="custom")
    assert logger.config_path == "logging.conf"


def test_custom_config_path():
    custom_config_path = "/path/to/custom/logging.conf"
    logger = Logger(name="custom", config_path=custom_config_path)
    assert logger.config_path == custom_config_path


@pytest.fixture()
def test_failed_config_loading(capsys):
    logger = Logger(name="custom", config_path="nonexistent.conf")
    logger.info("Test Info", {"test": "test"})
    content = capsys.readouterr().out

    # assert method should be called with the correct arguments
    assert "Failed to load logging configuration" in content
    assert "INFO - Test Info - {'test': 'test'}" in content
