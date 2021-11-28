import telebot
from telebot.types import CallbackQuery
from config import ALL_CONTENT_TYPES, GROUP_ID, TOKEN
from functionals import *

bot = telebot.TeleBot(TOKEN)


@bot.callback_query_handler(lambda call: call.data == 'channel_subscribe')
def channel_affirmative_reg(callback_query: CallbackQuery):
    if is_authenticated(callback_query):
        send_welcome_registration(callback_query)
    else:
        bot.answer_callback_query(callback_query_id=callback_query.id,
                                  show_alert=True, text="A'zo bo'lmadingiz!")


"""If you would like to use traditional registration """

# @bot.callback_query_handler(lambda call: call.data.startswith('reg_'))
# def user_registration(message):
#     first_name = message.from_user.first_name
#     if not is_none_data_user(message.from_user.id):
#         bot.send_message(message.from_user.id,
#                          f"Salom, {first_name}\nSiz bizda ro'yxatdan o'tgansiz! "
#                          f"/start ni bosing!",
#                          reply_markup=ReplyKeyboardRemove())
#     else:
#         bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.id,
#                               text="Ro'yxatdan o'tish boshlandi!")
#         markup = ReplyKeyboardMarkup(resize_keyboard=True)
#         markup.add("Qaytadan")
#         markup.add("Ortga")
#         msg = bot.send_message(message.from_user.id, "Ismingizni yozing: ", reply_markup=markup)
#         bot.register_next_step_handler(msg, get_name_registration)

#
# def get_name_registration(message):
#     try:
#         user_id = message.from_user.id
#         message_in = Usr(user_id)
#         user_dict[user_id] = message_in
#         foydalanuvchi = user_dict[user_id]
#         if message.text:
#             if message.text == "Qaytadan":
#                 msg = bot.send_message(message.from_user.id,
#                                        "Qaytadan ro'yxatdan o'tish boshlandi!\n"
#                                        "Ismingizni yozing: ")
#                 bot.register_next_step_handler(msg, get_name_registration)
#             elif message.text == "Ortga":
#                 send_welcome_registration(message)
#             else:
#                 foydalanuvchi.ism = message.text
#                 msg = bot.send_message(message.from_user.id, "Endi rasm jo'nating!")
#                 bot.register_next_step_handler(msg, get_photo_registration)
#         else:
#             msg = bot.send_message(message.from_user.id, "Iltimos faqat harflar yozing!")
#             bot.register_next_step_handler(msg, get_name_registration)
#     except Exception as e:
#         bot.send_message(message.from_user.id, f"Ro'yxatdan o'tish bekor qilindi!\n"
#                                                f"Регистрация отменена!\n\nКод: {e}")
#         send_welcome_registration(message)

#
# def get_photo_registration(message):
#     try:
#         user_id = message.from_user.id
#         foydalanuvchi = user_dict[user_id]
#         if message.text == "Qaytadan":
#             msg = bot.send_message(message.from_user.id,
#                                    "Qaytadan ro'yxatdan o'tish boshlandi!\n"
#                                    "Ismingizni yozing: ")
#             bot.register_next_step_handler(msg, get_name_registration)
#         elif message.text == "Ortga":
#             msg = bot.send_message(message.from_user.id,
#                                    "Ismingizni yozing: ")
#             bot.register_next_step_handler(msg, get_name_registration)
#         elif message.photo:
#             foydalanuvchi.rasm_id = message.photo[-1].file_id
#             keyboard = InlineKeyboardMarkup(row_width=2)
#             keyboard.add(
#                 InlineKeyboardButton(
#                     text="Qizlar",
#                     callback_data=f"finding_1"),
#                 InlineKeyboardButton(
#                     text="Yigitlar",
#                     callback_data=f"finding_2"))
#             keyboard.add(InlineKeyboardButton(
#                 text="Farqi yo'q",
#                 callback_data=f"finding_3"))
#             bot.send_message(message.from_user.id,
#                              "Kimlar bilan tanishmoqchisiz?", reply_markup=keyboard)
#
#         else:
#             msg = bot.send_message(message.from_user.id, "Menga faqat rasm yubor")
#             bot.register_next_step_handler(msg, get_photo_registration)
#
#     except Exception as e:
#         bot.send_message(message.from_user.id, f"Ro'yxatdan o'tish bekor qilindi!\n"
#                                                f"Регистрация отменена!\n\nКод: {e}")
#         send_welcome_registration(message)
#


@bot.callback_query_handler(lambda call: call.data.startswith('finding_'))
def reg_data_callback_finding(callback: CallbackQuery):
    user_confirm_registration(callback)


# @bot.callback_query_handler(lambda call: call.data.startswith('chatting_'))
# def reg_data_callback_chatting(callback: CallbackQuery):
#     chatting_user(callback)


@bot.message_handler(commands=["stop"])
def stop_chatting(message):
    clear_chatting_status(message)


@bot.message_handler(commands=["help"])
def stop_chatting(message):
    text = "Ushbu botdan foydalanish uchun *buyruqlar*:\n" \
           "/help - Yordamni chaqirish,\n" \
           "/next - Keyingi suhbatdoshga o'tish,\n" \
           "/stop - Qidiruvni to'xtatish,\n" \
           "/start - Botni qayta yoqish.\n"
    bot.send_message(message.from_user.id, text, parse_mode="Markdown")


@bot.message_handler(commands=["next"])
def next_chatting(message):
    clear_chatting_status(message)
    chatting_user_id = get_chatting_user_id(message)
    if not chatting_user_id:
        chatting_doesnt_exists = start_chatting_function(message)
        if chatting_doesnt_exists:
            bot.send_message(message.from_user.id, "Qidirilmoqda... Kuting")
            bot.send_message(message.from_user.id, "Sizni navbatga qo'ydik! Navbatni kuting")
        else:
            bot.send_message(message.from_user.id, "Navbatga qo'yilgansiz!\nBiroz kuting!")
    else:
        confirm_chatting_user(chatting_user_id[0], message.from_user.id)
        bot.send_message(message.from_user.id, "Topildi! Smsingizni yozing")


@bot.message_handler(commands=["start"])
def start_welcome_page(message):
    send_welcome_registration(message)


@bot.message_handler(content_types=ALL_CONTENT_TYPES)
def send_welcome_registration(msg):
    x = user_id_registration(msg.from_user.id, msg.from_user.username)
    if x:
        bot.forward_message(GROUP_ID, msg.from_user.id, msg.id)
        bot.send_message(GROUP_ID, f"Ushbu: @{x} botga qo'shildi")

    if is_authenticated(msg):
        if not have_data_user(msg.from_user.id):
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                InlineKeyboardButton(
                    text="Qizlar",
                    callback_data=f"finding_1"),
                InlineKeyboardButton(
                    text="Yigitlar",
                    callback_data=f"finding_2"))
            keyboard.add(InlineKeyboardButton(
                text="Muhim emas",
                callback_data=f"finding_3"))
            bot.send_message(msg.from_user.id,
                             f"Salom {msg.from_user.first_name}, \nKimlar bilan tanishmoqchisiz?",
                             reply_markup=keyboard)
        else:
            chat_id = get_active_chat_in_table(msg)
            chatting_user_id = get_chatting_user_tg_id(msg)
            if chatting_user_id:
                send_type_message(chatting_user_id, msg.json, msg.content_type)
            if not chat_id:
                bot.send_message(msg.from_user.id, "Iltimos /next knopkasini bosing!",
                                 reply_markup=ReplyKeyboardRemove())
    else:
        following_channel(msg)


if __name__ == '__main__':
    bot.polling()
