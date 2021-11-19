import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, InputMediaPhoto, ReplyKeyboardMarkup, \
    InputMediaVideo, InlineQuery, ReplyKeyboardRemove
from config import TOKEN, group_id, all_content_types
from functionals import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=all_content_types)
def send_welcome_registration(message):
    print("START")
    x = user_id_registration(message.from_user.id, message.from_user.username)
    if x:
        bot.forward_message(group_id, message.from_user.id, message.id)
        bot.send_message(group_id, f"Ushbu: @{x} botga qo'shildi")

    if is_authenticated(message):
        if is_none_data_user(message.from_user.id):
            text = "Xush kelibsiz! Ro'yxatdan o'ting!"
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton(
                text="Ro'yxatdan o'tish",
                callback_data=f"reg_{message.from_user.id}"))
            bot.send_message(message.from_user.id, text,
                             reply_markup=keyboard)
        else:
            # TODO NEED PASTE CHATING FUNCTION
            bot.send_message(message.from_user.id, "Tez kunda chat ishlaydi",
                             reply_markup=ReplyKeyboardRemove())
    else:
        text = "Kanalga a'zo bo'lish majburiy!"
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(
            text="1-chi kanal",
            url=f"https://t.me/{ref_url}"))
        keyboard.add(InlineKeyboardButton(
            text="A'zo bo'ldim✅",
            callback_data="channel_subscribe"))
        bot.send_message(message.from_user.id, text, reply_markup=keyboard)


@bot.callback_query_handler(lambda call: call.data == 'channel_subscribe')
def channel_affirmative_reg(callback_query: CallbackQuery):
    if is_authenticated(callback_query):
        send_welcome_registration(callback_query)
    else:
        bot.answer_callback_query(callback_query_id=callback_query.id,
                                  show_alert=True, text="A'zo bo'lmadingiz!")


@bot.callback_query_handler(lambda call: call.data.startswith('reg_'))
def user_registration_callback(callback):
    user_registration(callback, callback.message.id)


@bot.callback_query_handler(lambda call: call.data.startswith('qizlar_'))
def reg_data_1_callback(callback: CallbackQuery):
    user_confirm_registration(user_dict[callback.from_user.id], "qizlar_")


@bot.callback_query_handler(lambda call: call.data.startswith('yigitlar_'))
def reg_data_2_callback(callback: CallbackQuery):
    user_confirm_registration(user_dict[callback.from_user.id], "yigitlar_")


@bot.callback_query_handler(lambda call: call.data.startswith('farqi_yoq_'))
def reg_data_3_callback(callback: CallbackQuery):
    user_confirm_registration(user_dict[callback.from_user.id], "farqi_yoq_")


if __name__ == '__main__':
    bot.polling()
