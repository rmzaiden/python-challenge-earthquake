from helper.database import get_connection
import os
import sys

sys.path.append("../src")

DATABASE_URL = os.getenv("DATABASE_URL")


def create_database():
    """
    Creates a new database with the given name.

    Args:
        None

    Returns:
        None
    """
    db_name = "db_counterpart_challenge"
    engine = get_connection(DATABASE_URL)
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(f"CREATE DATABASE {db_name}")

if __name__ == "__main__":
    create_database()
