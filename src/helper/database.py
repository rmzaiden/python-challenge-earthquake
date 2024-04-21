import json
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_session_factory = None


def get_session_factory(database_url: str):
    """
    Returns a session factory for creating database sessions.

    Args:
        database_url (str): The URL of the database.

    Returns:
        SessionFactory: A session factory object.

    """
    global _session_factory
    if _session_factory is None:
        engine = get_connection(database_url)
        _session_factory = sessionmaker(bind=engine)
    return _session_factory


@contextmanager
def session_scope(database_url="DATABASE_URL"):
    """
    Context manager for managing a session with the database.

    Args:
        database_url (str): The URL of the database. Defaults to "DATABASE_URL".

    Yields:
        session: The session object.

    Raises:
        Any exception raised during the session.

    """
    session_local = get_session_factory(database_url)
    session = session_local()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_connection(database_url):
    """
    Establishes a connection to the database using the provided database URL.

    Args:
        database_url (str): The URL of the database.

    Returns:
        sqlalchemy.engine.Engine: The database connection engine.

    Raises:
        RuntimeError: If the database connection string is not found in the environment.
    """
    connection_string = os.getenv(database_url)
    if not connection_string:
        raise RuntimeError(
            f"Database connection string '{database_url}' not found in environment."
        )

    echo_sql = os.getenv("ECHO_SQL", "false").lower() == "true"
    execution_options = json.loads(os.getenv("SQLALCHEMY_EXECUTION_OPTIONS", "{}"))

    return create_engine(
        connection_string, echo=echo_sql, execution_options=execution_options
    )
