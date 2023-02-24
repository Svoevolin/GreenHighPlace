
import os

from app.models import CustomerModel as db

import telebot

# import urlextract

from datetime import date

from markups import InterNational as globalLanguage
from markups import ChoosedLanguage



def extractUniqueCode(text):
    return text.split()[1] if len(text.split()) > 1 else None

# language_msg_ids = {}

bot = telebot.TeleBot(os.getenv("TelegramBotToken"))

channelUsername = "@posmefPOFOPWEFBot"
@bot.message_handler(commands=['start'])
def start(message) -> None:

    unique_code = extractUniqueCode(message.text)
    print(unique_code)

    if unique_code == None:
        db.addCustomer(chatId=message.chat.id, username=message.chat.username, dateLogin=str(date.today().strftime("%d/%m/%Y")),
                     refCode='N/A')
    else:
        db.addCustomer(chatId=message.chat.id, username=message.chat.username, dateLogin=str(date.today().strftime("%d/%m/%Y")),
                     refCode=unique_code)

    bot.send_message(message.chat.id, globalLanguage.start_msg, reply_markup=globalLanguage.switchLanguage, parse_mode='MARKDOWN')



@bot.callback_query_handler(func=lambda call: True)
def language(call):

    localLanguage = ChoosedLanguage(call.data)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{localLanguage.answerLanguage}")
    bot.send_message(call.message.chat.id, localLanguage.welcomeText)
    bot.send_message(call.message.chat.id, localLanguage.askLocation)


if __name__ == '__main__':
    bot.infinity_polling()


# import telebot
# from telebot import types
# from telebot.types import InlineKeyboardButton
# from telegram_bot_pagination import InlineKeyboardPaginator
#
# bot = telebot.TeleBot("5756210383:AAE1IGrJxdQREI5vUegR3OQlJESPn56S-oU")
#
# last_msg = ''
#
# character_pages = [
#     '*Harry*\nHarry Potter is the Boy Who Lived, the Chosen One, the hero of the Wizarding world. He grew up with Muggles, and then came to Hogwarts where he faced dangers and terrors beyond his years. He, along with his friends Hermione Granger, Ron Weasley and Neville Longbottom, destroyed Voldemort’s Horcruxes. Harry faced Voldemort at the end of a climactic battle in Hogwarts castle and defeated him.',
#     '*Dumbledore*\nAlbus Dumbledore was the Headmaster of Hogwarts for close to forty years, a time period that encompassed both of Voldemort’s attempts to take over the Wizarding world. Considered to be the most powerful wizard of his time, Dumbledore was awarded the Order of Merlin, First Class, and was the Supreme Mugwump of the International Confederation of Wizards as well as the Chief Warlock of the Wizengamot.',
#     '*Voldemort*\nLord Voldemort, born Tom Marvolo Riddle, was the son of Merope Gaunt (a descendent of Salazar Slytherin) and Tom Riddle, a handsome, wealthy Muggle from Little Hangleton whom Merope ensnared with a love potion. When her husband found out she was a witch, he abandoned her while she was pregnant (HBP10). Tom’s mother died shortly after giving birth to him one December 31, living just long enough to name him Tom Riddle, after his father and Marvolo, after his grandfather.',
#     '*Snape*\nSeverus Snape was Potions Master, Defense Against the Dark Arts teacher, and Head of Slytherin at Hogwarts School of Witchcraft and Wizardry; he succeeded Dumbledore as Headmaster. He was personally killed by Lord Voldemort and his snake, Nagini.',
#     '*Sirius*\nSirius Black was James Potter’s closest friend, Harry Potter’s godfather, and an Animagus, who was falsely accused of betrayal and murder and imprisoned in Azkaban.',
#     '*Hermione*\nResourceful, principled and brilliant, Hermione Jean Granger is easily the brightest witch of her generation. She, along with Ron Weasley, is one of Harry Potter’s closest friends. She is also Muggle-born (her parents were dentists – PS12), and so is a living, breathing example of the fallacy of pureblood wizard supremacy.',
#     '*Ron*\nRon Weasley is Harry Potter’s best friend and the youngest son of Molly and Arthur Weasley. The story of Ron’s life is one of being overshadowed by his family and friends, yet it is Ron’s heart and humor that have solidified his friendships and given those around him the support they needed to carry through (BLC). ',
#     '*Draco*\nDraco Malfoy is the son and only child of Lucius and Narcissa Malfoy and was a student at Hogwarts in the same year as Harry Potter. He is a rival of Harry, actively trying to undermine him in any way he can. Draco has white-blond hair and a pale, pointed face. He owns an eagle owl which made almost daily deliveries of sweets from home. Draco became the Slytherin Quidditch Seeker after his father made a generous donation of Nimbus 2001 brooms to the team (CS7).',
#     '*Hagrid*\nRubeus Hagrid is a half-giant with shaggy hair and a “wild, tangled beard” (PS1) who serves as the Keeper of Keys and Grounds, Gamekeeper, and Care of Magical Creatures professor at Hogwarts (PS4, PA6).',
#     '*Dobby*\nDobby was a house-elf, for years indentured to the Malfoy family, until his admiration for Harry Potter goaded him into trying to warn Harry against coming to school in his second year because he knew what Lucius was planning with the diary.',
#     '*Moody*\nAlastor “Mad-Eye” Moody is a retired Auror, considered one of the best Dark Wizard catchers the Ministry has ever had.',
# ]
# @bot.message_handler(func=lambda message: True)
# def get_character(message):
#     send_character_page(message)
#
#
# @bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='character')
# def characters_page_callback(call):
#     page = int(call.data.split('#')[1])
#     bot.delete_message(
#         call.message.chat.id,
#         call.message.message_id
#     )
#     send_character_page(call.message, page)
#
#
# def send_character_page(message, page=1):
#     paginator = InlineKeyboardPaginator(
#         len(character_pages),
#         current_page=page,
#         data_pattern='character#{page}'
#     )
#
#     paginator.add_before(
#         InlineKeyboardButton('Like', callback_data='show_tovar_1'),
#         InlineKeyboardButton('Dislike', callback_data='dislike#{}'.format(page))
#     )
#     paginator.add_after(InlineKeyboardButton('Go back', callback_data='back'))
#
#     bot.send_message(
#         message.chat.id,
#         character_pages[page-1],
#         reply_markup=paginator.markup,
#         parse_mode='Markdown'
#     )


# off_markup = types.ReplyKeyboardRemove(selective=False)
#
# menu_admin = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# itembtn1 = types.KeyboardButton('kek')
# itembtn2 = types.KeyboardButton('lol')
# menu_admin.add(itembtn1,itembtn2)
#
# menu_admin1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# itembtn1 = types.KeyboardButton('admin1')
# itembtn2 = types.KeyboardButton('admin2')
# menu_admin1.add(itembtn1,itembtn2)
#
# url_btn = types.InlineKeyboardMarkup(row_width=1)
# itembtn1 = types.InlineKeyboardButton(text='Русский', url="https://github.com/kde2podfreebsd/SaveTGBot/blob/main/app/bot/markups.py")
# url_btn.add(itembtn1)
#
# callbtn = types.InlineKeyboardMarkup(row_width=1)
# itembtn1 = types.InlineKeyboardButton(text='Русский', callback_data="1")
# itembtn2 = types.InlineKeyboardButton(text='Узбек', callback_data="2")
# callbtn.add(itembtn1, itembtn2)
#
# callbtn1 = types.InlineKeyboardMarkup(row_width=1)
# itembtn1 = types.InlineKeyboardButton(text='МУЖИК', callback_data="3")
# itembtn2 = types.InlineKeyboardButton(text='МЕГА МУЖИК', callback_data="4")
# callbtn1.add(itembtn1, itembtn2)
#
# callbtn2 = types.InlineKeyboardMarkup(row_width=1)
# itembtn1 = types.InlineKeyboardButton(text='Канал', url="https://t.me/boshki_test_channel")
# itembtn2 = types.InlineKeyboardButton(text='Проверить саб', callback_data="is_sub")
# callbtn2.add(itembtn1, itembtn2)
#
# def extract_unique_code(text):
#     return text.split()[1] if len(text.split()) > 1 else None



# @bot.message_handler(commands=['start'])
# def start(message):
#     unique_code = extract_unique_code(message.text)
#     if unique_code is not None:
#         bot.send_message(message.chat.id, unique_code)
#     else:
#         bot.send_message(message.chat.id, "реф кода нет")

    # print(message.text)
    # msg = bot.send_message(message.chat.id, "test", reply_markup=callbtn2, parse_mode='MARKDOWN')

# @bot.message_handler(content_types=["text"])
# def echo(message):
#     if message.text == 'kek':
#         msg = bot.send_message(message.chat.id, "Введи сколько тебе лет",reply_markup=menu_admin1)
#         bot.register_next_step_handler(msg, next_step)
#
#     if message.text == 'lol':
#         bot.send_message(message.chat.id, "ты отправил лол",reply_markup=callbtn)
#
#
#
# def next_step(message):
#     age = message.text
#     bot.send_message(message.chat.id, f'тебе {age} лет', reply_markup=url_btn)
#
#
# @bot.callback_query_handler(func=lambda call:True)
# def callback_handler(call):
#     if call.data == "1":
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="ты крут")
#         bot.send_message(call.message.chat.id, 'ТЫ РУССКИЙ')
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=callbtn1)
#         bot.answer_callback_query(call.id, text="МЕГА РУССИЧ!")
# @bot.callback_query_handler(func=lambda call:True)
# def callback_handler(call):
#     if call.data == "is_sub":
#         status = bot.get_chat_member("@boshki_test_channel", call.message.chat.id)
#         if status.status == 'left':
#             # bot.delete_message(call.message.chat.id, message_id=last_msg)
