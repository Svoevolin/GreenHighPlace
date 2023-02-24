from telebot import types


class InterNational():
    start_msg = '''
Hi!
Choose language

Привет!
Выбери язык
    '''

    switchLanguage = types.InlineKeyboardMarkup(row_width=1)
    languageEN = types.InlineKeyboardButton("English", callback_data="EN")
    languageRU = types.InlineKeyboardButton("Русский", callback_data="RU")
    switchLanguage.add(languageEN, languageRU)


class ChoosedLanguage():

    def __init__(self, language):

        match language:

            case "RU":
                self.welcomeText = '''
Привет!
Ты в крутом магазине на крутом острове
Можешь сделать заказ и оформить доставку'''

                self.answerLanguage = '''
Выбран язык Русский
Ты можешь изменить его в профиле
'''
                self.askLocation = '''
Напишите свой адрес или отправьте свою геолокацию
'''
            case "EN":
                self.welcomeText = '''
Hello!
You are in the cool boshkiShop on cool Island
You can make an order and do delivery
'''
                self.answerLanguage = '''
Choosed language English
You can change it in your profile
'''
                self.askLocation = '''
Write your adress or send geolocation
'''

            case _:
                print("Language Error")



