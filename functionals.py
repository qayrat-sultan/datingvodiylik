from main import bot
from config import ref_url
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, InputMediaPhoto, ReplyKeyboardMarkup, InputMediaVideo
from db import connection, cursor


def is_authenticated(msg):
    try:
        if bot.get_chat_member(f'@{ref_url}', user_id=msg.from_user.id).status in ('member', 'administrator', 'creator'):
            return True
        else:
            raise("Ne avtorizovan")
    except Exception as ex:
        return False





def user_id_registration(tg_id, tg_username):
    cursor.execute(f"SELECT telegram_id, username FROM users_users WHERE telegram_id={tg_id};")
    telegram_user_id = cursor.fetchone()
    if not telegram_user_id:
        sql = """INSERT INTO users_users (telegram_id, username, checking) VALUES (%s,%s,%s);"""
        sql_insert = (tg_id, tg_username, True)
        cursor.execute(sql, sql_insert)
        connection.commit()
        return tg_username
    else:
        cursor.execute(f"Update users_users set checking = {True}, username = '{tg_username}' where telegram_id = {tg_id}")
        connection.commit()
    return None