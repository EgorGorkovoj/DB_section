from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema_db.core.config import settings

engine = create_engine(settings.database_url(), echo=True)

Session = sessionmaker(bind=engine)
