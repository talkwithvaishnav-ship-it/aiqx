from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH
import os

session_string = os.getenv("TELETHON_SESSION")

client = TelegramClient(
    StringSession(session_string),
    API_ID,
    API_HASH
)
