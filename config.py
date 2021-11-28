import logging
import datetime

from configparser import ConfigParser
from environs import Env

env = Env()
env.read_env()

SUBSCRIBE_CHANNELS = "vodiylik",
TOKEN = env.str("BOT_TOKEN")
REF_URL = env.str("REF_URL")
GROUP_ID = env.int("GROUP_ID")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_DATABASE = env.str("DB_DATABASE")

SEARCH_SLEEP_TIME = env.int("SEARCH_SLEEP_TIME")

formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
logging.basicConfig(
    filename=f'bot-from-{datetime.datetime.now().date()}.log',
    filemode='w',
    format=formatter,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARNING
)


ALL_CONTENT_TYPES = ["text", "audio", "photo", "sticker",
                     "video", "video_note", "voice", "location",
                     "contact", "new_chat_members", "left_chat_member",
                     "new_chat_title", "new_chat_photo", "delete_chat_photo",
                     "group_chat_created", "supergroup_chat_created",
                     "channel_chat_created", "migrate_to_chat_id",
                     "migrate_from_chat_id", "pinned_message"]


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
