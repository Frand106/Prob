from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from userbot.config import (API_ID, API_HASH)

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print(client.session.save())
