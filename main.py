import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, InputMediaPhoto, ReplyKeyboardMarkup, InputMediaVideo, InlineQuery
from config import TOKEN, group_id, all_content_types
from functionals import *


bot = telebot.TeleBot(TOKEN)
user_dict = {}


class Usr:
    def __init__(self, user_id):
        self.user_id = user_id
        self.ism = None
        self.rasm_id = None
        self.yonalish = None


@bot.message_handler(func=lambda msg: msg.text == "Ro'yxatdan o'tish")
def registration_user(message):
    first_name = message.from_user.first_name
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Ro'yxatdan o'tish")
    cursor.execute(f"SELECT * from users_users WHERE telegram_id = {message.from_user.id}")
    data = cursor.fetchone()
    data = None
    if data:
        bot.send_message(message.from_user.id,
                         f"Hozirgi Sizning ma'lumotlaringiz:\n\n"
                         f"FIO: {data[0]}\nGruppa: {data[1]}-18\nYo'nalish: {data[2]}!\n\n"
                         f"Ma'lumotlar to'g'rimi\nВерны ли данные?",
                         reply_markup=markup)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Qaytadan")
        keyboard.add("Ortga")
        msg = bot.send_message(message.from_user.id,
                               "Ismingizni yozing!", reply_markup=keyboard)
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
                msg = bot.send_message(message.from_user.id, "Guruhni tanlang!\nВыберите группу")
                bot.register_next_step_handler(msg, get_name)
            else:
                foydalanuvchi.ism = message.text
                msg = bot.send_message(message.from_user.id, "Endi rasm jo'nating!")
                bot.register_next_step_handler(msg, get_rasm)
        else:
            msg = bot.send_message(message.from_user.id, "Iltimos faqat harflar yozing!")
            bot.register_next_step_handler(msg, get_name)
    except Exception as e:
        bot.send_message(message.from_user.id, f"Ro'yxatdan o'tish bekor qilindi!\nРегистрация отменена!\n\nКод: {e}")
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
                msg = bot.send_message(message.from_user.id, "Guruhni tanlang!\nВыберите группу")
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
                bot.send_message(message.from_user.id, "Kimlar bilan tanishmoqchisiz?", reply_markup=keyboard)
            else:
                msg = bot.send_message(message.from_user.id, "Menga rasm yubor")
                bot.register_next_step_handler(msg, get_rasm)
    except Exception as e:
        bot.send_message(message.from_user.id, f"Ro'yxatdan o'tish bekor qilindi!\nРегистрация отменена!\n\nКод: {e}")
        send_welcome_registration(message)


@bot.message_handler(content_types=all_content_types)
def send_welcome_registration(message):
    print("START")
    x = user_id_registration(message.from_user.id, message.from_user.username)

    if is_authenticated(message):
        text = "Xush kelibsiz! Ro'yxatdan o'ting!"
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Ro'yxatdan o'tish")
        bot.send_message(message.from_user.id, text,
                         reply_markup=markup)
    else:
        text = "Kanalga a'zo bo'lish majburiy!"
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(
            text="1-chi kanal",
            url=f"https://t.me/{ref_url}"))
        keyboard.add(InlineKeyboardButton(
            text="A'zo bo'ldim✅",
            callback_data="channel_kino"))
        bot.send_message(message.from_user.id, text, reply_markup=keyboard)
    print("GGGGGG")
    if x:
        bot.forward_message(group_id, message.from_user.id, message.id)
        bot.send_message(group_id, f"Ushbu: @{x} botga qo'shildi")


@bot.callback_query_handler(lambda call: call.data == 'channel_kino')
def channel_affirmative_kino(callback_query: CallbackQuery):
    if is_authenticated(callback_query):
        send_welcome_registration(callback_query)
    else:
        bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True, text="A'zo bo'lmadingiz!")


@bot.callback_query_handler(lambda call: call.data.startswith('qizlar_'))
def reg_data_1(callback_query: CallbackQuery):
    user_confirm_registration(user_dict, callback_query, "qizlar_")


@bot.callback_query_handler(lambda call: call.data.startswith('yigitlar_'))
def reg_data_2(callback_query: CallbackQuery):
    user_confirm_registration(user_dict, callback_query, "yigitlar_")


@bot.callback_query_handler(lambda call: call.data.startswith('farqi_yoq_'))
def reg_data_1(callback_query: CallbackQuery):
    user_confirm_registration(user_dict, callback_query, "farqi_yoq_")


if __name__ == '__main__':
    bot.polling()
