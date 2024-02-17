from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DATABASE = {
        "username": os.environ["DB_USERNAME"],
        "password": os.environ["DB_USERNAME_PASSWORD"],
        "server": os.environ["DB_SERVER"],
        "port": os.environ["DB_PORT"],
        "db_name": os.environ["DB_NAME"],
    }


settings = Settings()
