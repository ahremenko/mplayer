from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()
USER = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')
HOST = os.environ.get('DB_HOST')
PORT = os.environ.get('DB_PORT')
DATABASE = os.environ.get('DB_DATABASE')

# use alembic only!


def get_engine():
    if HOST is None or USER is None or DATABASE is None or PORT is None or PASSWORD is None:
        return None
    engine = create_async_engine(
        f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
        echo=False,
        isolation_level="AUTOCOMMIT"
    )
    return engine


def get_sync_engine():
    if HOST is None or USER is None or DATABASE is None or PORT is None or PASSWORD is None:
        return None
    engine = create_engine(
        f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
        echo=False,
        isolation_level="AUTOCOMMIT"
    )
    return engine


def get_engine_string():
    return f"@{HOST}:{PORT}/{DATABASE}"

