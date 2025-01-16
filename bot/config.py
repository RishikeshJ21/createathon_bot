import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
GRAPH_API_URL = "https://graph.facebook.com/v15.0"
