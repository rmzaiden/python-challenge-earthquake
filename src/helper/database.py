import json
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


def create_session(database_url: str) -> Session:
    session = sessionmaker(bind=get_connection(database_url))
    return session()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = create_session("DATABASE_URL")
    try:
        yield session
    finally:
        session.close()


def get_connection(database_url):
    mssql_connection_string = os.getenv(database_url)

    if not mssql_connection_string:
        raise RuntimeError(f"Database Connection .env: '{database_url}' not found")

    echo_sql = os.getenv("ECHO_SQL", "false").lower() == "true"
    sqlalchemy_execution_options = (
        json.loads(os.getenv("SQLALCHEMY_EXECUTION_OPTIONS", "{}"))
        if os.getenv("SQLALCHEMY_EXECUTION_OPTIONS")
        else None
    )

    return create_engine(
        mssql_connection_string,
        echo=echo_sql,
        execution_options=sqlalchemy_execution_options,
    )


def is_sqlite(session: Session = None):
    return session.get_bind().name == "sqlite"
