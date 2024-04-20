"""Test the main module."""
import pytest

from src.main import hello


@pytest.fixture()
def test_hello(capsys):
    """Test the hello function."""
    hello()
    captured = capsys.readouterr().out
    assert "Hello World!" in captured
