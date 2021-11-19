from main import bot, send_welcome_registration
from config import ref_url
from db import connection, cursor

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup

user_dict = {}


class Usr:
    def __init__(self, user_id):
        self.user_id = user_id
        self.ism = None
        self.rasm_id = None
        self.yonalish = None


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


def user_confirm_registration(user_obj, yonalish):
    user_obj.yonalish = yonalish.replace("_", "")
    cursor.execute(f"UPDATE users_users SET user_fullname='{user_obj.ism}', "
                   f"user_photo='{user_obj.rasm_id}', "
                   f"user_yonalish='{user_obj.yonalish}' "
                   f"WHERE telegram_id = {user_obj.user_id};")


def is_none_data_user(tg_id):
    cursor.execute("SELECT user_fullname, user_photo, user_yonalish FROM "
                   f"users_users WHERE telegram_id={tg_id};")
    x = cursor.fetchone()
    return not all(x)


def user_registration(message, msg_id):
    first_name = message.from_user.first_name
    if not is_none_data_user(message.from_user.id):
        bot.send_message(message.from_user.id,
                         f"Salom, {first_name}\nSiz bizda ro'yxatdan o'tgansiz! "
                         f"/start ni bosing!",
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
                              text="Ismingizni yozing!")
        msg = bot.send_message(message.from_user.id,
                               "Ismingizni yozing!")
        bot.register_next_step_handler(msg, get_name)


def get_name(message):
    try:
        user_id = message.from_user.id
        message_in = Usr(user_id)
        user_dict[user_id] = message_in
        foydalanuvchi = user_dict[user_id]
        if message.text:
            if message.text == "Qaytadan":
                bot.send_message(message.from_user.id, "Bekor qilindi!")
                send_welcome_registration(message)
            elif message.text == "Ortga":
                msg = bot.send_message(message.from_user.id, "Guruhni tanlang!\n"
                                                             "Выберите группу")
                bot.register_next_step_handler(msg, get_name)
            else:
                foydalanuvchi.ism = message.text
                msg = bot.send_message(message.from_user.id, "Endi rasm jo'nating!")
                bot.register_next_step_handler(msg, get_rasm)
        else:
            msg = bot.send_message(message.from_user.id, "Iltimos faqat harflar yozing!")
            bot.register_next_step_handler(msg, get_name)
    except Exception as e:
        bot.send_message(message.from_user.id, f"Ro'yxatdan o'tish bekor qilindi!\n"
                                               f"Регистрация отменена!\n\nКод: {e}")
        send_welcome_registration(message)


def get_rasm(message):
    try:
        user_id = message.from_user.id
        foydalanuvchi = user_dict[user_id]
        if message.text:
            if message.text == "Qaytadan":
                bot.send_message(message.from_user.id, "Bekor qilindi!")
                send_welcome_registration(message)
            elif message.text == "Ortga":
                msg = bot.send_message(message.from_user.id,
                                       "Guruhni tanlang!\nВыберите группу")
                bot.register_next_step_handler(msg, get_name)
        else:
            if message.photo:
                foydalanuvchi.rasm_id = message.photo[-1].file_id
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(
                    InlineKeyboardButton(
                        text="Qizlar",
                        callback_data=f"qizlar_{user_id}"),
                    InlineKeyboardButton(
                        text="Yigitlar",
                        callback_data=f"yigitlar_{user_id}"))
                keyboard.add(InlineKeyboardButton(
                    text="Farqi yo'q",
                    callback_data=f"farqi_yoq_{user_id}"))
                bot.send_message(message.from_user.id,
                                 "Kimlar bilan tanishmoqchisiz?", reply_markup=keyboard)
            else:
                msg = bot.send_message(message.from_user.id, "Menga rasm yubor")
                bot.register_next_step_handler(msg, get_rasm)
    except Exception as e:
        bot.send_message(message.from_user.id, f"Ro'yxatdan o'tish bekor qilindi!\n"
                                               f"Регистрация отменена!\n\nКод: {e}")
        send_welcome_registration(message)
