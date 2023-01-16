from telethon import TelegramClient

from funcs import ConfigParser

client = TelegramClient("user", ConfigParser.getint("Telegram", "api_id"), ConfigParser.get("Telegram", "api_hash"))
client.start()
