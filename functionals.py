import datetime
import logging

from constants import get_yonalish
from main import bot
from config import REF_URL, SUBSCRIBE_CHANNELS
from db import connection, cursor

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# user_dict = {}
#
#
# class Usr:
#     def __init__(self, user_id):
#         self.user_id = user_id
#         self.ism = None
#         self.rasm_id = None
#         self.yonalish = None


group_to_process_method = {
    "audio": bot.send_audio,
    "sticker": bot.send_sticker,
    "video": bot.send_video,
    "voice": bot.send_voice,
    "document": bot.send_document
}


def send_type_message(msg_user_id, json_dict: dict, content):
    json_content = json_dict[content]

    bot.send_message(390736292, json_content)
    bot.send_message(390736292, json_dict)
    if content == 'text':
        bot.send_message(msg_user_id, json_content)
    elif content == 'photo':
        bot.send_photo(msg_user_id, json_content[-1]['file_id'])
    elif content == 'location':
        bot.send_location(msg_user_id, json_content['latitude'],
                          json_content['longitude'])
    elif content == 'contact':
        bot.send_contact(msg_user_id, json_content['phone_number'],
                         json_content['first_name'])
    else:
        group_to_process_method[content](msg_user_id, json_content['file_id'])
    # except Exception as e:
    #     logging.info(f"USER WAS BLOKED BOT: {msg_user_id}. \n{e}")
    #     cursor.execute("UPDATE users_users SET checking = False WHERE "
    #                    f"telegram_id = {msg_user_id};")
    #     cursor.execute("UPDATE users_chatting SET status = False WHERE "
    #                    f"tg_id = {msg_user_id} or right_id = {msg_user_id}")


def is_authorized(msg):
    try:
        if bot.get_chat_member(f'@{REF_URL}', user_id=msg.from_user.id).status in \
                ('member', 'administrator', 'creator'):
            return True
        else:
            raise "Unauthorized"
    except Exception as e:
        logging.info(f"Unauthorizing user: {e}")
        return False


def following_channel(message):
    text = "Kanalga a'zo bo'lish majburiy!"
    keyboard = InlineKeyboardMarkup(row_width=1)
    for num, i in enumerate(SUBSCRIBE_CHANNELS):
        keyboard.add(InlineKeyboardButton(
            text=f"{str(num + 1)}-chi kanal",
            url=f"https://t.me/{REF_URL}"))
    keyboard.add(InlineKeyboardButton(
        text="A'zo bo'ldim✅",
        callback_data="channel_subscribe"))
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


# noinspection PyBroadException
def user_id_registration(tg_id, tg_username):
    try:
        cursor.execute(f"SELECT telegram_id, username FROM users_users WHERE telegram_id={tg_id};")
        telegram_user_id = cursor.fetchone()
        if not telegram_user_id:
            sql = "INSERT INTO users_users (telegram_id, username, checking) " \
                  "VALUES (%s,%s,%s);"
            sql_insert = (tg_id, tg_username, True)
            cursor.execute(sql, sql_insert)
            connection.commit()
            return tg_username
        else:
            cursor.execute(f"Update users_users set checking = {True}, "
                           f"username = '{tg_username}' where telegram_id = {tg_id}")
            connection.commit()
        return None
    except Exception as e:
        logging.error(f"USER ID REGISTRATION FUNCTION DOESN'T WORK: {e}")
        return None
#
#
# def gettin_chatting_user_photo(tg_id):
#     cursor.execute(f"SELECT user_photo FROM users_users WHERE telegram_id={tg_id}")
#     photo = cursor.fetchone()
#     return photo[0]
#
#
# def chatting_user(callback):
#     tg_id = callback.data.replace("chatting_", "")
#     profile_photo = gettin_chatting_user_photo(tg_id)
#     text = "XABARINGIZNI YOZING"
#     bot.edit_message_media(media=InputMediaPhoto(media=profile_photo, caption=text),
#                            chat_id=callback.from_user.id,
#                            message_id=callback.message.id,
#                            reply_markup=None)
#     confirm_chatting_user(callback.from_user.id, tg_id)


def confirm_chatting_user(column_id, right_tg_id):
    cursor.execute("UPDATE users_chatting SET "
                   "status=true, "
                   f"right_id={right_tg_id} WHERE id={column_id}")


def user_confirm_registration(callback):
    route = int(callback.data.replace("finding_", ""))
    timestamp = callback.message.date
    created_at = datetime.datetime.utcfromtimestamp(timestamp)
    cursor.execute(f"UPDATE users_users SET username='{callback.from_user.username}', "
                   "checking=TRUE, "
                   f"user_fullname='{callback.from_user.first_name} {callback.from_user.last_name}', "
                   f"user_yonalish={route}, "
                   f"created_at='{created_at}' "
                   f"WHERE telegram_id = {callback.from_user.id};")
    bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.id,
                          text=f"Sizga qidiruvda {get_yonalish(route)}lar chiqadi",
                          reply_markup=None)
    # bot.send_photo(user_obj.user_id, user_obj.rasm_id,
    #                f"Ismi: {user_obj.ism},\n"
    #                f"Tanishuv: {get_yonalish(user_obj.yonalish)}",
    #                reply_markup=ReplyKeyboardRemove())


def have_data_user(tg_id):
    cursor.execute("SELECT user_yonalish FROM "
                   f"users_users WHERE telegram_id={tg_id};")
    x = cursor.fetchone()
    return all(x)  # if one item in x[i]==None -> all(x) returning False


def start_chatting_function(message):
    tg_sex = get_user_gender(message.from_user.id)
    cursor.execute("INSERT INTO users_chatting (tg_id, tg_sex, tg_route) "
                   f"VALUES ({message.from_user.id}, "
                   f"{tg_sex if tg_sex is not None else 3}, (SELECT user_yonalish "
                   f"FROM users_users WHERE telegram_id={message.from_user.id})) RETURNING id;")
    chatting_id = cursor.fetchone()
    return chatting_id
    # except Exception as e:
    #     logging.error(f"START CHATTING FUNCTION ERROR: {e}")


def get_chatting_user_is_existing(message):
    # TODO NEED SEARCH from gender
    cursor.execute("SELECT * FROM users_chatting WHERE status=false "
                   f"and right_id IS NULL and tg_id NOT IN ({message.from_user.id});")
    chat_id = cursor.fetchone()
    return chat_id


def get_active_chat_in_table(message):
    user_tg_id = message.from_user.id
    cursor.execute("SELECT * FROM users_chatting WHERE status=true and "
                   f"(tg_id={user_tg_id} or right_id={user_tg_id});")
    chat_id = cursor.fetchone()
    return chat_id


def get_chatting_user_tg_id(message):
    cursor.execute("SELECT tg_id, right_id FROM users_chatting WHERE "
                   f"(tg_id={message.from_user.id} or "
                   f"right_id={message.from_user.id}) and "
                   f"status=true;")
    xs = cursor.fetchone()
    if xs:
        if message.from_user.id == xs[0]:
            return xs[1]
        else:
            return xs[0]
    return None


def clear_chatting_status(message):
    user_id = message.from_user.id
    cursor.execute("SELECT id, tg_id, right_id FROM users_chatting WHERE "
                   f"(tg_id={user_id} or right_id={user_id}) and status=true")
    ids = cursor.fetchone()
    if ids:
        cursor.execute(f"UPDATE users_chatting SET status=false WHERE id={ids[0]};")


def get_user_gender(tg_id):
    cursor.execute(f"SELECT gender FROM users_users WHERE telegram_id={tg_id}")
    gender = cursor.fetchone()
    return gender[0]
