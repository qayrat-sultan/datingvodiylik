import logging
import datetime

from configparser import ConfigParser

TOKEN = "2078942594:AAFzEOk4Z3vNdCyM60tU_-IECyGE3GGT44g"

formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
logging.basicConfig(
    filename=f'bot-from-{datetime.datetime.now().date()}.log',
    filemode='w',
    format=formatter,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARNING
)

# TOKEN = os.environ.get("token")

ref_url = 'vodiylik'
group_id = -1001145839692

all_content_types = ["text", "audio", "photo", "sticker",
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





