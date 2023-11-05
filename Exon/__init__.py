"""

STATUS: Code is working. ✅

"""



"""

BSD 2-Clause License



Copyright (C) 2022, SOME-1HING [https://github.com/SOME-1HING]



Credits:-

    I don't know who originally wrote this code. If you originally wrote this code, please reach out to me. 



All rights reserved.



Redistribution and use in source and binary forms, with or without

modification, are permitted provided that the following conditions are met:



1. Redistributions of source code must retain the above copyright notice, this

   list of conditions and the following disclaimer.



2. Redistributions in binary form must reproduce the above copyright notice,

   this list of conditions and the following disclaimer in the documentation

   and/or other materials provided with the distribution.



THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"

AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE

IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE

DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE

FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL

DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR

SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER

CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,

OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE

OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""



import logging

import os

import sys

import time

from pyrogram.types import Message

from inspect import getfullargspec

from pyrogram import Client, filters

from redis import StrictRedis

from aiohttp import ClientSession

import telegram.ext as tg

from telethon import TelegramClient

from Python_ARQ import ARQ

from telethon.sessions import MemorySession

import Keep_alive

from Exon.services.quoteapi import Quotly

import spamwatch



Keep_alive.keep_alive()



StartTime = time.time()

USE_JOIN_LOGGER = True



# enable logging

FORMAT = "[Shikimori] %(message)s"

logging.basicConfig(

    handlers=[logging.FileHandler("bot_logs.txt"), logging.StreamHandler()],

    level=logging.INFO,

    format=FORMAT,

    datefmt="[%X]",

)

logging.getLogger("pyrogram").setLevel(logging.INFO)

logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)



LOGGER = logging.getLogger('[Shikimori]')

LOGGER.info("Shikimori is starting. | Built by SOME1HING. | Licensed under GPLv3.")

LOGGER.info("Handled by: github.com/SOME-1HING (t.me/SOME1HING)")



async def eor(msg: Message, **kwargs):

    func = (

        (msg.edit_text if msg.from_user.is_self else msg.reply)

        if msg.from_user

        else msg.reply

    )

    spec = getfullargspec(func.__wrapped__).args

    return await func(**{k: v for k, v in kwargs.items() if k in spec})





# if version < 3.6, stop bot.

if sys.version_info[0] < 3 or sys.version_info[1] < 6:

    LOGGER.error(

        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."

    )

    quit(1)



ENV = bool(os.environ.get("ENV", True))



if ENV:

    TOKEN = os.environ.get("TOKEN", None)



    try:

        OWNER_ID = int(os.environ.get("OWNER_ID", None))

    except ValueError:

        raise Exception("Your OWNER_ID env variable is not a valid integer.")

     

    ERROR_LOG_CHANNEL = os.environ.get("ERROR_LOG_CHANNEL", None)

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)

    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)



    try:

        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())

        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())

    except ValueError:

        raise Exception("Your sudo or dev users list does not contain valid integers.")



    try:

        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())

    except ValueError:

        raise Exception("Your support users list does not contain valid integers.")



    try:

        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())

    except ValueError:

        raise Exception("Your whitelisted users list does not contain valid integers.")



    try:

        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())

    except ValueError:

        raise Exception("Your tiger users list does not contain valid integers.")

    SPAMWATCH_API = ""

    LOG_CHANNEL = os.environ.get("LOG_CHANNEL", None)

    WEBHOOK = bool(os.environ.get("WEBHOOK", False))

    URL = os.environ.get("URL", "")  # Does not contain token

    PORT = int(os.environ.get("PORT", 5000))

    CERT_PATH = os.environ.get("CERT_PATH")

    API_ID = os.environ.get("API_ID", None)

    API_HASH = os.environ.get("API_HASH", None)

    DB_URL = os.environ.get("DATABASE_URL")

    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)

    ARQ_API = os.environ.get("ARQ_API_BASE_URL", None)

    LOAD = os.environ.get("LOAD", "").split()

    NO_LOAD = os.environ.get("NO_LOAD", None).split()

    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))

    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))

    WORKERS = int(os.environ.get("WORKERS", 8))

    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")

    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", True)

    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")

    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)

    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)

    AI_API_KEY = os.environ.get("AI_API_KEY", None)

    API_WEATHER = os.environ.get("API_WEATHER", None)

    WALL_API = os.environ.get("WALL_API", None)

    REDIS_URL = os.environ.get("REDIS_URL")

    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)

    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None)

    ARQ_API_KEY = os.environ.get("ARQ_API", None)

    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)

    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)

    APOD_API_KEY = os.environ.get("APOD_API_KEY", None)

    ANIME_NAME = os.environ.get("ANIME_NAME", "Shikimori's Not Just a Cutie")

    START_MEDIA = os.environ.get("START_MEDIA", "https://telegra.ph/file/9235d57807362b4e227a3.mp4")

    BOT_USERNAME = os.environ.get("BOT_USERNAME", "micchon_shikimori_bot")

    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "Shikimori_bot_Updates")

    ALIVE_MEDIA = os.environ.get("ALIVE_MEDIA", "https://telegra.ph/file/2b04f7812f22b983f8a10.mp4")

    BOT_ID = os.environ.get("BOT_ID", "5169508699")

    STATS_IMG = os.environ.get("STATS_IMG", None)

    NETWORK = os.environ.get("NETWORK", None)

    NETWORK_USERNAME = os.environ.get("NETWORK_USERNAME", None)

    MEDIA_GM = os.environ.get("MEDIA_GM", None)

    MEDIA_GN = os.environ.get("MEDIA_GN", None)

    MEDIA_HELLO = os.environ.get("MEDIA_HELLO", None)

    MEDIA_BYE = os.environ.get("MEDIA_BYE", None)

    INLINE_IMG = os.environ.get("INLINE_IMG", None)

    OWNER_WELCOME_MEDIA = os.environ.get("OWNER_WELCOME_MEDIA", None)

    EVENT_LOGS = os.environ.get("EVENT_LOGS", None) 



    try:

        WHITELIST_CHATS = {int(x) for x in os.environ.get('WHITELIST_CHATS', "").split()}

    except ValueError:

        raise Exception(

            "Your blacklisted chats list does not contain valid integers.")



    try:

        BLACKLIST_CHATS = {int(x) for x in os.environ.get('BLACKLIST_CHATS', "").split()}

    except ValueError:

        raise Exception(

            "Your blacklisted chats list does not contain valid integers.")



else:

    from Config import Development as Config



    TOKEN = Config.TOKEN



    try:

        OWNER_ID = int(Config.OWNER_ID)

    except ValueError:

        raise Exception("Your OWNER_ID variable is not a valid integer.")

        

    SPAMWATCH_API = ""

    JOIN_LOGGER = Config.JOIN_LOGGER

    ERROR_LOG_CHANNEL = Config.ERROR_LOG_CHANNEL

    OWNER_USERNAME = Config.OWNER_USERNAME



    try:

        DRAGONS = set(int(x) for x in Config.DRAGONS or [])

        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])

    except ValueError:

        raise Exception("Your sudo or dev users list does not contain valid integers.")



    try:

        DEMONS = set(int(x) for x in Config.DEMONS or [])

    except ValueError:

        raise Exception("Your support users list does not contain valid integers.")



    try:

        WOLVES = set(int(x) for x in Config.WOLVES or [])

    except ValueError:

        raise Exception("Your whitelisted users list does not contain valid integers.")



    try:

        TIGERS = set(int(x) for x in Config.TIGERS or [])

    except ValueError:

        raise Exception("Your tiger users list does not contain valid integers.")



    LOG_CHANNEL = Config.LOG_CHANNEL

    WEBHOOK = Config.WEBHOOK

    URL = Config.URL

    PORT = Config.PORT

    CERT_PATH = Config.CERT_PATH

    API_ID = Config.API_ID

    API_HASH = Config.API_HASH

    HEROKU_API_KEY = Config.HEROKU_API_KEY

    HEROKU_APP_NAME = Config.HEROKU_APP_NAME

    DB_URI = Config.SQLALCHEMY_DATABASE_URI

    LOAD = Config.LOAD

    NO_LOAD = Config.NO_LOAD

    DEL_CMDS = Config.DEL_CMDS

    STRICT_GBAN = Config.STRICT_GBAN

    WORKERS = Config.WORKERS

    BAN_STICKER = Config.BAN_STICKER

    ALLOW_EXCL = Config.ALLOW_EXCL

    CASH_API_KEY = Config.CASH_API_KEY

    TIME_API_KEY = Config.TIME_API_KEY

    AI_API_KEY = Config.AI_API_KEY

    API_WEATHER = Config.API_WEATHER

    WALL_API = Config.WALL_API

    SUPPORT_CHAT = Config.SUPPORT_CHAT

    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT

    APOD_API_KEY = Config.APOD_API_KEY

    REDIS_URL = Config.REDIS_URL

    ANIME_NAME = Config.ANIME_NAME

    START_MEDIA = Config.START_MEDIA

    BOT_USERNAME = Config.BOT_USERNAME

    UPDATE_CHANNEL = Config.UPDATE_CHANNEL

    ALIVE_MEDIA = Config.ALIVE_MEDIA

    BOT_ID = Config.BOT_ID

    STATS_IMG = Config.STATS_IMG

    NETWORK = Config.NETWORK

    NETWORK_USERNAME = Config.NETWORK_USERNAME

    MEDIA_GM = Config.MEDIA_GM

    MEDIA_GN = Config.MEDIA_GN

    MEDIA_HELLO = Config.MEDIA_HELLO

    MEDIA_BYE = Config.MEDIA_BYE

    INLINE_IMG = Config.INLINE_IMG

    OWNER_WELCOME_MEDIA = Config.OWNER_WELCOME_MEDIA



    try:

        WHITELIST_CHATS = {int(x) for x in os.environ.get('WHITELIST_CHATS', "").split()}

    except ValueError:

        raise Exception(

            "Your blacklisted chats list does not contain valid integers.")



    try:

        BLACKLIST_CHATS = {int(x) for x in os.environ.get('BLACKLIST_CHATS', "").split()}

    except ValueError:

        raise Exception(

            "Your blacklisted chats list does not contain valid integers.")



DRAGONS.add(OWNER_ID)

DEV_USERS.add(OWNER_ID)

DEV_USERS.add(5700727404)

SUDOERS = filters.user()





REDIS = StrictRedis.from_url(REDIS_URL,decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("Your redis server is now alive!")

except BaseException:

    raise Exception("Your redis server is not alive, please check again.")

    

finally:

   REDIS.ping()
   LOGGER.info("Your redis server is now alive!")





from Exon.modules.sql import SESSION



defaults = tg.Defaults(run_async=True)

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)

telethn = TelegramClient(MemorySession(), API_ID, API_HASH)

dispatcher = updater.dispatcher



aiohttpsession = ClientSession()



ARQ_API_URL = "https://arq.hamker.in"



# Aiohttp Client

print("[INFO]: INITIALZING AIOHTTP SESSION")

session = ClientSession()

# ARQ Client

print("[INFO]: INITIALIZING ARQ CLIENT")

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)



pbot = Client("ShikimoriPyro", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)



DRAGONS = list(DRAGONS) + list(DEV_USERS)

DEV_USERS = list(DEV_USERS)

WOLVES = list(WOLVES)

DEMONS = list(DEMONS)

TIGERS = list(TIGERS)



if not SPAMWATCH_API:

    sw = None

    LOGGER.warning("SpamWatch API key missing! recheck your config.")

else:

    sw = spamwatch.Client(SPAMWATCH_API)





# Load at end to ensure all prev variables have been set

from Shikimori.modules.helper_funcs.handlers import (

    CustomCommandHandler,

    CustomMessageHandler,

    CustomRegexHandler,

)



# make sure the regex handler can take extra kwargs

tg.RegexHandler = CustomRegexHandler

tg.CommandHandler = CustomCommandHandler

tg.MessageHandler = CustomMessageHandler





quotly = Quotly()
