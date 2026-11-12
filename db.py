import os
from sqlalchemy import URL
from sqlmodel import Session, create_engine


def create_database_engine():
    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "111111"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "velosiped_drive"),
    )

    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


engine = create_database_engine()


def get_session():
    return Session(engine)