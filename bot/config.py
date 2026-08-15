import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ACR_HOST = os.getenv("ACR_HOST")
ACR_ACCESS_KEY = os.getenv("ACR_ACCESS_KEY")
ACR_ACCESS_SECRET = os.getenv("ACR_ACCESS_SECRET")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Please set it in your .env file.")