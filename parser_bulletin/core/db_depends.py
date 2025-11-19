from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = create_engine(settings.database_url, echo=True)

SessionLocal = sessionmaker(bind=engine)


def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with SessionLocal() as session:
            return func(*args, session=session, **kwargs)
    return wrapper
