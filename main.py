import asyncio
import datetime
import io
import logging
import os
import time

import pytz
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

from funcs import ConfigParser, get_weather, get_image

while not os.path.exists("user.session"):
    logging.warning("You need execute log_in.py file first!")
    time.sleep(5)

logging.basicConfig(level=logging.INFO)
client = TelegramClient("user", ConfigParser.getint("Telegram", "api_id"), ConfigParser.get("Telegram", "api_hash"))
client.start()


async def main():
    logging.info("Bot started")
    while True:
        logging.info("Getting weather...")
        weather = get_weather()
        logging.info("Render image...")
        avatar = get_image(
            datetime.datetime.now(tz=pytz.timezone(ConfigParser.get("Data", "locale"))), weather.temp
        )

        if weather.weather is None:
            await client.send_message("me", weather.raw + "\n\nНе определена погода")
        else:
            print(weather.weather)

        avatar_file = io.BytesIO()
        avatar.save(avatar_file, "JPEG")
        avatar_file.seek(0)

        logging.info("Clear avatars...")
        await client(DeletePhotosRequest(await client.get_profile_photos('me')))
        logging.info("Sending photo...")
        await client(UploadProfilePhotoRequest(await client.upload_file(avatar_file)))
        logging.info("Picture changed")

        d = datetime.datetime.now(tz=pytz.timezone(ConfigParser.get("Data", "locale")))
        await asyncio.sleep(60 - d.second)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
