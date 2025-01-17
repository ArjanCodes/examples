import os

import psycopg2
from dotenv import load_dotenv
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from ..config import Environment, settings

load_dotenv()


# When using local development, use the service account credentials
if settings.ENVIRONMENT == Environment.DEVELOPMENT.value:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../../service-account.json"
    )


def connect_to_db():
    """
    Connects to the database based on the environment.
    """
    db_pass = settings.DB_PASSWORD
    db_user = settings.DB_USER
    db_name = settings.DB_NAME
    db_host = settings.DB_HOST
    db_port = settings.DB_PORT

    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
    )

    database_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(
        url=database_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine, SessionLocal


def connect_to_cloud_sql() -> Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """

    instance_connection_name = settings.DB_HOST
    db_user = settings.DB_USER
    db_pass = settings.DB_PASSWORD
    db_name = settings.DB_NAME

    ip_type = IPTypes.PRIVATE if settings.DB_PRIVATE_IP else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    connection_pool = create_engine(
        "postgresql+pg8000://",
        creator=lambda: connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        ),
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
    )

    # Create a sessionmaker for the engine
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection_pool)

    return connection_pool, SessionLocal


def connect_to_local_db():  # pragma: no cover
    """
    Initializes a connection pool for a local Postgres instance.
    """
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal
