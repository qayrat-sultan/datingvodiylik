import datetime

from constants import get_yonalish
from main import bot
from config import REF_URL
from db import connection, cursor

from telebot.types import ReplyKeyboardRemove

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


def user_id_registration(tg_id, tg_username):
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
