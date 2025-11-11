from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker, DeclarativeBase, Mapped, mapped_column, declared_attr
)
from sqlalchemy import func

from azure.core.exceptions import HttpResponseError

from typing import Annotated
from datetime import datetime

from logger import client, logger


def get_db_url():
    url = "sqlite:///./db.sqlite3"
    try:
        secret = client.get_secret(SECRET_NAME).value
        if secret:
            url = secret
    except HttpResponseError as e:
        logger.exception(e)
    finally:
        return url


SECRET_NAME = "database-uri"
DATABASE_URL = get_db_url()


engine = create_engine(DATABASE_URL)


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
