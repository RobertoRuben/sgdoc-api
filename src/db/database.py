from urllib.parse import quote_plus
from sqlmodel import SQLModel, create_engine
from src.config.settings import settings
from src.model.entity import *

user = quote_plus(settings.POSTGRES_USER)
password = quote_plus(settings.POSTGRES_PASSWORD)

postgres_url = f"postgresql://{user}:{password}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    