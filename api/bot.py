import logging
import logging.config
import os
import time
from datetime import datetime
import pytz
from typing import Union, Optional, AsyncGenerator

from fastapi import FastAPI, Request, Response
from pyrogram import Client, __version__, types
from pyrogram.raw.all import layer

from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL
from utils import temp

# Logging setup
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

# FastAPI app
app = FastAPI()

class Bot(Client):
    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
            in_memory=True
        )

    async def start(self):
        temp.START_TIME = time.time()
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.BOT = self
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} 𝖶𝗂𝗍𝗁 𝖥𝗈𝗋 𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆 v{__version__} (Layer {layer}) 𝖲𝗍𝖺𝗋𝗍𝖾𝖽 𝖮𝗇 @{me.username}.")
        logging.info(LOG_STR)
        await self.send_message(chat_id=LOG_CHANNEL, text=f"{me.first_name} 𝖶𝗂𝗍𝗁 𝖥𝗈𝗋 𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆 v{__version__} (Layer {layer}) 𝖲𝗍𝖺𝗋𝗍𝖾𝖽 𝖮𝗇 @{me.username}")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1

bot_instance = Bot()

# This is a placeholder. Pyrogram does not support webhooks natively.
# You must use polling on a VPS or switch to python-telegram-bot for webhooks.
@app.post("/webhook")
async def handle_webhook(request: Request):
    # Pyrogram does not support webhook updates natively.
    # This is just a placeholder to show how you would handle it if it did.
    return Response(status_code=200)

@app.on_event("startup")
async def startup_event():
    await bot_instance.start()

@app.on_event("shutdown")
async def shutdown_event():
    await bot_instance.stop()

# For health checks
@app.get("/health")
async def health_check():
    return {"status": "ok"}
    
