from sqlmodel import create_engine

from app.configs.settings import settings

database_url = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    settings.DATABASE["username"],
    settings.DATABASE["password"],
    settings.DATABASE["server"],
    settings.DATABASE["port"],
    settings.DATABASE["db_name"],
)


engine = create_engine(database_url, echo=True)
