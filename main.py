import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, InputMediaPhoto, ReplyKeyboardMarkup, InputMediaVideo, InlineQuery
from config import TOKEN, group_id
from functionals import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda msg: msg.text == "🔙Bosh sahifa")
def send_welcome_homepage(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Ro'yxatdan o'tish")
    bot.send_message(message.from_user.id, "Avval ro'yhatdan o'ting", reply_markup=markup)


@bot.message_handler(commands=["start"])
def send_welcome_registration(message):
    if is_authenticated(message):
        bot.send_message(message.from_user.id, "Xush kelibsiz")
        # first_name = message.from_user.first_name
        # x = user_id_registration(message.from_user.id, message.from_user.username)
        # send_welcome_homepage(message)
        # if x:
        #     bot.send_message(message.chat.id, f"Salom, {first_name}!\nKinolar olamiga xush kelibsiz!")
        #     bot.forward_message(group_id, message.chat.id, message.id)
        #     bot.send_message(group_id, f"Ushbu: @{x} botga qo'shildi")



@bot.callback_query_handler(lambda call: call.data == 'channel_kino')
def channel_affirmative_kino(callback_query: CallbackQuery):
    if is_authenticated(callback_query):
        send_welcome_homepage(callback_query)
    else:
        bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True, text="A'zo bo'lmadingiz!")



if __name__ == '__main__':
    bot.polling()
