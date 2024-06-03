import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST=os.environ.get("POSTGRES_HOST")
POSTGRES_PORT=os.environ.get("POSTGRES_PORT")
POSTGRES_USER=os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB=os.environ.get("POSTGRES_DB")

SUBNET_ID = os.environ.get("SUBNET_ID")

POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_URL_INI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_SSL="root.crt"

IAM_TOKEN = os.environ.get("IAM_TOKEN")
FOLDER_ID = os.environ.get("FOLDER_ID")

SALT_SIZE=int(os.environ.get("SALT_SIZE"))