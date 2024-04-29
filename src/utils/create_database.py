import os
import sys

from dotenv import load_dotenv
from sqlalchemy.sql import text

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

load_dotenv()

from helper.database import get_connection


def create_database():
    """
    Creates a new database with the given name.
    """
    db_name = "db_counterpart_challenge"
    engine = get_connection("DATABASE_MASTER_URL")
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{db_name}') BEGIN CREATE DATABASE {db_name}; END;"))


if __name__ == "__main__":
    create_database()
