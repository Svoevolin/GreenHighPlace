import telebot
from python_paginations import InlineKeyboardPaginator
from telebot.types import InlineKeyboardButton
import os
from dotenv import load_dotenv
from app.models import CustomerModel as db
from app.models import ProductModel as pm

config = load_dotenv()

bot = telebot.TeleBot(os.getenv('TelegramBotToken'))

class sliderProductPaginator(InlineKeyboardPaginator):
    first_page_label = ''
    previous_page_label = '-'
    next_page_label = '+'
    last_page_label = ''

def textProduct(name, infoAbout, price, language):

    if language == "RU":
        return f'''{name}
{infoAbout}

Доставка по всему острову
1 грамм - {price} BATH'''

    elif language == "EN":
        return f'''{name}
{infoAbout}

Delivery on the whole Island
1 gram - {price} BATH'''
def sliderProduct(page, name, price, language):

    paginator = sliderProductPaginator(
        page_count=2500,
        current_page=page,
        data_pattern='coast#' + name + '#{page}'
    )
    paginator.current_page_label = '{}' + '| {}'.format(int(paginator.current_page) * price)


    if language == "RU":

        toChooseNumberOf = InlineKeyboardButton('Указать количество', callback_data='toChooseNumberOf')
        toOrderDelivery = InlineKeyboardButton('Заказать доставку', callback_data='toOrderDelivery')
        toBin = InlineKeyboardButton('В корзину', callback_data='toBin')
        toBackButton = InlineKeyboardButton('Назад', callback_data='toShop')
        paginator.add_after(toChooseNumberOf, toOrderDelivery, toBin, toBackButton)

    elif language == "EN":

        toChooseNumberOf = InlineKeyboardButton('Indicate quantity', callback_data='toChooseNumberOf')
        toOrderDelivery = InlineKeyboardButton('Order delivery', callback_data='toOrderDelivery')
        toBin = InlineKeyboardButton('Add to cart', callback_data='toBin')
        toBackButton = InlineKeyboardButton('Back', callback_data='toShop')
        paginator.add_after(toChooseNumberOf, toOrderDelivery, toBin, toBackButton)

    return paginator.markup

@bot.callback_query_handler(func=lambda call: True)
def characters_page_callback(call):

    if call.data.split('#')[0] == 'coast':

        bot.delete_message(call.message.chat.id, call.message.message_id)

        send_character_page(call.message, int(call.data.split('#')[1]))

    # if call.data.split('#')[0] == 'productName':
    #     bot.edit_message_text()


def send_character_page(message, page=1, name):

    # paginator.current_page_label = '{}'# + f'/{len(character_pages)}'

    bot.send_message(
        message.chat.id,
        textShop(db.getLanguage(message.chat.id)),
        reply_markup=sliderShop(page, pm.getProducts(), db.getLanguage(message.chat.id)),
        parse_mode='Markdown'
    )


bot.polling()