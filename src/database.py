from sqlalchemy import create_engine, func
from sqlalchemy.orm import (
    sessionmaker, DeclarativeBase, Mapped, mapped_column, declared_attr
)

from typing import Annotated
from datetime import datetime
import os

from logger import client


SECRET_NAME = "database-uri"
ENV = os.environ.get("ENV", "PROD")


def get_db_engine():
    if ENV == "DEV":
        return create_engine("sqlite:///./db.sqlite3")
    elif ENV == "PROD":
        secret = client.get_secret(SECRET_NAME).value
        if secret:
            return create_engine(secret)


engine = get_db_engine()


SessionLocal = sessionmaker(autoflush=False, bind=engine)


created_at = Annotated[
    datetime, mapped_column(default=func.now(), nullable=False)
]

updated_at = Annotated[
    datetime, mapped_column(default=func.now(), onupdate=func.now(), nullable=False)
]


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
