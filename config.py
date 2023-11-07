from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    LOGGER = True

    API_ID = int(getenv("API_ID", 6))
    API_HASH = getenv("API_HASH", None)
    ARQ_API_KEY = "HDEBTP-URNMLY-BUQXRQ-RRSUPF-ARQ"
    STRING_SESSION = getenv("STRING_SESSION", None)
    SPAMWATCH_API = None
    TOKEN = getenv("TOKEN", None)
    OWNER_ID = int(getenv("OWNER_ID", "6495264484"))  # sᴛᴀʀᴛ @Exon_Robot ᴛʏᴘᴇ /id
    OWNER_USERNAME = getenv("OWNER_USERNAME", "YeahKAKASHl")
    SUPPORT_CHAT = getenv("SUPPORT_CHAT", "rose_orianalogs")
    LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002143522204"))
    MONGO_URI = getenv("MONGO_DB_URI")
    REDIS_URL = "redis://default:SeeHVAqRRbzHNEQ1gFac5rZIui5whbpQ@redis-17680.c289.us-west-1-2.ec2.cloud.redislabs.com:17680"
    DATABASE_URL = getenv("DATABASE_URL")

    # ɴᴏ ᴇᴅɪᴛ ᴢᴏɴᴇ
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
