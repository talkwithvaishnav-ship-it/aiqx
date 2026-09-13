from telethon import TelegramClient
from config import API_ID, API_HASH

client = TelegramClient(
    "quotex_session_final",
    API_ID,
    API_HASH
)
