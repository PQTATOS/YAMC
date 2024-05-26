import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST=os.environ.get("POSTGRES_HOST")
POSTGRES_PORT=os.environ.get("POSTGRES_PORT")
POSTGRES_USER=os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB=os.environ.get("POSTGRES_DB")

POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
POSTGRES_SSL="root.crt"

SALT_SIZE=int(os.environ.get("SALT_SIZE"))