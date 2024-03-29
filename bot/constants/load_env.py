import os
from dotenv import load_dotenv

from bot.exceptions.env_error import EnvError

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

if None in [API_ID, API_HASH, BOT_TOKEN, MONGO_CONNECTION_STRING]:
    raise EnvError("Set .env file with constants like it is in .env.example")
