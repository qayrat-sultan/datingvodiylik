import datetime

from constants import get_yonalish
from main import bot
from config import REF_URL, SUBSCRIBE_CHANNELS
from db import connection, cursor

from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, InputMediaPhoto

user_dict = {}


class Usr:
    def __init__(self, user_id):
        self.user_id = user_id
        self.ism = None
        self.rasm_id = None
        self.yonalish = None


def is_authenticated(msg):
    try:
        if bot.get_chat_member(f'@{REF_URL}', user_id=msg.from_user.id).status in \
                ('member', 'administrator', 'creator'):
            return True
        else:
            raise "Unauthorized"
    except Exception as ex:
        print(ex)
        return False


def following_channel(message):
    text = "Kanalga a'zo bo'lish majburiy!"
    keyboard = InlineKeyboardMarkup(row_width=1)
    for num, i in enumerate(SUBSCRIBE_CHANNELS):
        keyboard.add(InlineKeyboardButton(
            text=f"{str(num+1)}-chi kanal",
            url=f"https://t.me/{REF_URL}"))
    keyboard.add(InlineKeyboardButton(
        text="A'zo bo'ldim✅",
        callback_data="channel_subscribe"))
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


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
        return e


def gettin_chatting_user_photo(tg_id):
    cursor.execute(f"SELECT user_photo FROM users_users WHERE telegram_id={tg_id}")
    photo = cursor.fetchone()
    return photo[0]


def chatting_user(callback):
    tg_id = callback.data.replace("chatting_", "")
    profile_photo = gettin_chatting_user_photo(tg_id)
    text = "XABARINGIZNI YOZING"
    bot.edit_message_media(media=InputMediaPhoto(media=profile_photo, caption=text),
                           chat_id=callback.from_user.id,
                           message_id=callback.message.id,
                           reply_markup=None)
    print("LEFT", callback.from_user.id, "RIGHT: ", tg_id)
    confirm_chatting_user(callback.from_user.id, tg_id)


def confirm_chatting_user(left_tg_id, right_tg_id):
    print("left: ", left_tg_id, "right: ", right_tg_id)
    cursor.execute("UPDATE users_chatting SET status=false "
                   f"WHERE left_id={left_tg_id} or right_id={right_tg_id}")
    cursor.execute("UPDATE users_users SET chatting=false "
                   f"WHERE telegram_id={left_tg_id};")
    cursor.execute("UPDATE users_users SET "
                   f"chatting=true "
                   f"WHERE telegram_id={left_tg_id};")
    cursor.execute("UPDATE users_users SET "
                   f"chatting=true "
                   f"WHERE telegram_id={right_tg_id};")
    cursor.execute("INSERT INTO users_chatting (left_id, right_id) "
                   f"VALUES ({left_tg_id}, {right_tg_id}) RETURNING ID;")
    x = cursor.fetchone()
    print("AAAAAAAAAAA", x)


def user_confirm_registration(user_obj, callback):
    user_obj.yonalish = int(callback.data.replace("finding_", ""))
    timestamp = callback.message.date
    created_at = datetime.datetime.utcfromtimestamp(timestamp)
    cursor.execute(f"UPDATE users_users SET username='{callback.from_user.username}', "
                   "checking=TRUE, "
                   f"user_fullname='{user_obj.ism}', "
                   f"user_photo='{user_obj.rasm_id}', "
                   f"user_yonalish={user_obj.yonalish}, "
                   f"created_at='{created_at}' "
                   f"WHERE telegram_id = {user_obj.user_id};")
    bot.clear_step_handler_by_chat_id(user_obj.user_id)
    bot.edit_message_text(chat_id=user_obj.user_id, message_id=callback.message.id,
                          text="Muvaffaqiyatli ro'yxatdan o'tdingiz!",
                          reply_markup=None)
    bot.send_photo(user_obj.user_id, user_obj.rasm_id,
                   f"Ismi: {user_obj.ism},\n"
                   f"Tanishuv: {get_yonalish(user_obj.yonalish)}",
                   reply_markup=ReplyKeyboardRemove())


def is_none_data_user(tg_id):
    cursor.execute("SELECT user_fullname, user_photo, user_yonalish FROM "
                   f"users_users WHERE telegram_id={tg_id};")
    x = cursor.fetchone()
    return not all(x)


def get_random_user_info(msg):
    tg_user_id = msg.from_user.id
    cursor.execute(f"SELECT user_yonalish "
                   f"FROM users_users "
                   f"WHERE telegram_id={tg_user_id};")
    user_yonalish_info = cursor.fetchone()
    print(user_yonalish_info[0], "YONALISH INFO")
    yonalish = get_yonalish(user_yonalish_info[0])
    print(yonalish, "YONALISH")

    if yonalish == "Qizlar":
        cursor.execute(f"SELECT telegram_id, user_fullname, "
                       f"user_photo, gender FROM users_users "
                       f"WHERE gender=1 AND checking=TRUE;")
        odam = cursor.fetchone()
        return odam
    elif yonalish == "Yigitlar":
        cursor.execute(f"SELECT telegram_id, user_fullname, "
                       f"user_photo, gender FROM users_users "
                       f"WHERE gender=2 AND checking=TRUE;")
        odam = cursor.fetchone()
        return odam
    else:
        cursor.execute(f"SELECT telegram_id, user_fullname, "
                       f"user_photo, gender FROM users_users "
                       f"WHERE checking=TRUE "
                       f"ORDER BY random() LIMIT 1;")
        odam = cursor.fetchone()
        return odam


def start_chatting_function(message):
    timestamp = message.date
    created_at = datetime.datetime.utcfromtimestamp(timestamp)
    cursor.execute("INSERT INTO users_chats (left_user, created_at) "
                   f"VALUES ({message.from_user.id}, '{created_at}');")


def get_chatting_user_id(message):
    bot.send_message(message.from_user.id, "Qidirilmoqda... Kuting")
    cursor.execute("SELECT * FROM users_users WHERE chatting=FALSE and "
                   f"telegram_id NOT IN ({message.from_user.id}) "
                   "ORDER BY random();")
    chat_id = cursor.fetchone()
    print("GET_CHATTING_USER_ID ", chat_id)
    return chat_id


def get_active_chat_table(message):
    cursor.execute("SELECT * FROM users_chats WHERE active=true and "
                   f"(left_user={message.from_user.id} or right_user={message.from_user.id});")
    chat_id = cursor.fetchone()

    return chat_id


def text_chatting_user_id(message):
    cursor.execute("SELECT * FROM users_chatting WHERE "
                   f"(left_id={message.from_user.id} or "
                   f"right_id={message.from_user.id}) and "
                   f"status=true;")
    x = cursor.fetchone()
    print(x)
    if message.from_user.id == x[1]:
        return x[2]
    else:
        return x[1]


def clear_chatting_status(message):
    user_id = message.from_user.id
    cursor.execute("SELECT left_id, right_id FROM users_chatting WHERE "
                   f"(left_id={user_id} or right_id={user_id}) and status=true")
    ids = cursor.fetchone()
    print(ids)
    if ids:
        cursor.execute("UPDATE users_users SET chatting=false "
                       f"WHERE telegram_id={ids[0]} or telegram_id={ids[1]}")
