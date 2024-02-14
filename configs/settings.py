from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = {
    "username": os.environ['DB_USERNAME'],
    "password": os.environ['DB_USERNAME_PASSWORD'],
    "url": os.environ['DB_URL'],
    "db_name": os.environ['DB_NAME']
}