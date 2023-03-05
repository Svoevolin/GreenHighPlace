import os
from app.models import CustomerModel as db
from app.models import ProductModel as pm
from app.models import CartModel as cart
from app.models import ActiveOrderModel as ao
from app.models import RefusalOrderModel as ro
from app.models import CompleteOrderModel as co
from app.models import AdminModel as am
from app.models import postModel as post
from app.models import NewProductModel as npm
import telebot
from dotenv import load_dotenv
from datetime import date
from tools import get_address
import markups as mk
from telebot.apihelper import ApiTelegramException


import pathlib

config = load_dotenv()


adminPostSaleChecker = dict()
adminAddProductChecker = dict()

def extractUniqueCode(text):
    return text.split()[1] if len(text.split()) > 1 else None


bot = telebot.TeleBot(os.getenv('TelegramBotToken'))


# #
# id = pm.addProduct('Шишки еловые', 100)
# pm.setType(id, 'video')
# pm.setMedia(id, '/home/fake_svoevolin/Desktop/tgBot_BOSHKI_PHUKET/Media/01.mp4')
# pm.setInfoAbout(id, 'Хорошие шишки бери')
#
# #
# id = pm.addProduct('Шишки кедровые', 150)
# pm.setType(id, 'video')
# pm.setMedia(id, '/home/fake_svoevolin/Desktop/tgBot_BOSHKI_PHUKET/Media/02.mp4')
# pm.setInfoAbout(id, 'Хорошие шишки бери')
#
# id = pm.addProduct('Шишки разные', 100)
# pm.setType(id, 'video')
# pm.setMedia(id, '/home/fake_svoevolin/Desktop/tgBot_BOSHKI_PHUKET/Media/03.mp4')
# pm.setInfoAbout(id, 'Хорошие шишки бери')
# #
# #
# id = pm.addProduct('Шишки махна', 104)
# pm.setType(id, 'video')
# pm.setMedia(id, '/home/fake_svoevolin/Desktop/tgBot_BOSHKI_PHUKET/Media/04.mp4')
# pm.setInfoAbout(id, 'Хорошие шишки бери')
#
# id = pm.addProduct('Шишки просто', 120)
# pm.setType(id, 'video')
# pm.setMedia(id, '/home/fake_svoevolin/Desktop/tgBot_BOSHKI_PHUKET/Media/01.mp4')
# pm.setInfoAbout(id, 'Хорошие шишки бери')
#
#
# id = pm.addProduct('Шишки китайские', 40)
# pm.setType(id, 'video')
# pm.setMedia(id, '/home/fake_svoevolin/Desktop/tgBot_BOSHKI_PHUKET/Media/02.mp4')
# pm.setInfoAbout(id, 'Хорошие шишки бери')
#
# id =  pm.addProduct('Шишки плохие', 130)
# pm.setType(id, 'video')
# pm.setMedia(id, '/home/fake_svoevolin/Desktop/tgBot_BOSHKI_PHUKET/Media/03.mp4')
# pm.setInfoAbout(id, 'Хорошие шишки бери')
#
# id = pm.addProduct('Шишки хорошие', 70)
# pm.setType(id, 'video')
# pm.setMedia(id, '/home/fake_svoevolin/Desktop/tgBot_BOSHKI_PHUKET/Media/04.mp4')
# pm.setInfoAbout(id, 'Хорошие шишки бери')


# co.switcherActiveToComplete(ao.getActiveOrder(1))
# ro.switcherActiveToRefusal(ao.getActiveOrder(2), "Бан по причине пидарас")
@bot.message_handler(commands=['start'])
def start(message) -> None:
    if not am.checkAdmin(chatId=message.chat.id):

        unique_code = extractUniqueCode(message.text)

        if db.addCustomer(chatId=message.chat.id, username=message.chat.username,
                          dateLogin=str(date.today().strftime("%d/%m/%Y"))) == 1:
            db.setRef(chatId=message.chat.id, refCode=unique_code if unique_code is not None else 'N/A')

        bot.send_message(message.chat.id, mk.start_msg, reply_markup=mk.switchLanguage, parse_mode='MARKDOWN')

    else:
        bot.send_message(chat_id=message.chat.id,
                         text=mk.helloBoss(),
                         reply_markup=mk.helloMenu())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if not am.checkAdmin(chatId=message.chat.id):
        if message.text == mk.writeLocationRU.text or message.text == mk.writeLocationEN.text:
            msg = bot.send_message(message.chat.id, mk.inviteToWriteAddress(db.getLanguage(chatId=message.chat.id)),
                                   parse_mode='MARKDOWN')
            bot.register_next_step_handler(msg, stepByInviteToWriteAddress)

        if message.text == mk.passLocationRU.text or message.text == mk.passLocationEN.text:
            bot.send_message(message.chat.id, "🔧",
                             reply_markup=mk.menuBuyProfile(db.getLanguage(chatId=message.chat.id)),
                             parse_mode='MARKDOWN')

            bot.send_message(message.chat.id, mk.indexAddreessLater(db.getLanguage(chatId=message.chat.id)),
                             reply_markup=mk.toShop(db.getLanguage(chatId=message.chat.id)),
                             parse_mode='MARKDOWN')

        if message.text == mk.toProfileMarkupRU or message.text == mk.toProfileMarkupEN:
            bot.send_message(chat_id=message.chat.id, text=mk.getInfoProfile(language=db.getLanguage(message.chat.id),
                                                                             address=db.getAddress(message.chat.id),
                                                                             comment=db.getComment(message.chat.id)),
                             reply_markup=mk.profileMenu(db.getLanguage(message.chat.id)),
                             parse_mode='MARKDOWN')

        if message.text == mk.toBuyMarkupRU or message.text == mk.toBuyMarkupEN:
            bot.send_message(
                chat_id=message.chat.id,
                text=mk.textShop(db.getLanguage(message.chat.id), pm.getProducts()),
                reply_markup=mk.sliderShop(len(pm.getProducts()) // 2, pm.getProducts(),
                                           db.getLanguage(message.chat.id)),
                parse_mode='MARKDOWN'
            )

        if message.text == mk.toAdminText:
            msg = bot.send_message(chat_id=message.chat.id, text=mk.toEnterPasswordText())
            bot.register_next_step_handler(msg, stepToEnterPassword)

    elif am.checkAdmin(chatId=message.chat.id):
        if message.text == "На главную":
            bot.send_message(chat_id=message.chat.id,
                             text=mk.helloBoss(),
                             reply_markup=mk.helloMenu())


def stepToEnterPassword(message):
    if message.text == mk.password:
        am.addAdmin(message.chat.id)
        bot.send_message(chat_id=message.chat.id, text=mk.passwordCorrectText(), reply_markup=mk.mainAdmin())
    else:
        bot.send_message(chat_id=message.chat.id, text=mk.passwordUncorrectText())


def stepByInviteToWriteAddress(message):
    db.setAddress(chatId=message.chat.id, location=message.text)
    db.setComment(chatId=message.chat.id, comment=None)

    msg = bot.send_message(chat_id=message.chat.id,
                           text=mk.addressInfo(db.getLanguage(chatId=message.chat.id),
                                               db.getAddress(chatId=message.chat.id))
                                + "\n\n" + mk.toCommentAddress(db.getLanguage(chatId=message.chat.id)),
                           reply_markup=mk.toCommentAdress(db.getLanguage(chatId=message.chat.id)),
                           parse_mode='MARKDOWN')

    bot.register_next_step_handler(msg, stepByGetAddress)


def stepByGetAddress(message):
    db.setComment(chatId=message.chat.id, comment=message.text)
    # тут смайлик
    bot.send_message(message.chat.id, "🔧", reply_markup=mk.menuBuyProfile(db.getLanguage(chatId=message.chat.id)),
                     parse_mode='MARKDOWN')

    bot.send_message(message.chat.id, mk.addressAddedSuccessfully(db.getLanguage(chatId=message.chat.id)),
                     reply_markup=mk.toShop(db.getLanguage(message.chat.id)), parse_mode="MARKDOWN")


@bot.callback_query_handler(func=lambda call: True)
def language(call):
    print(call.data)
    if call.data == "EN" or call.data == "RU":
        db.setLanguage(chatId=call.message.chat.id, language=call.data)

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.welcomeText(db.getLanguage(chatId=call.message.chat.id)) + "\n\n" +
                              mk.askLocation(db.getLanguage(chatId=call.message.chat.id)),
                         reply_markup=mk.menuLocation(db.getLanguage(chatId=call.message.chat.id)),
                         parse_mode='MARKDOWN')

    if call.data == "passCommentAdress":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        bot.send_message(call.message.chat.id, "🔧",
                         reply_markup=mk.menuBuyProfile(db.getLanguage(chatId=call.message.chat.id)),
                         parse_mode='MARKDOWN')

        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.addressAddedSuccessfully(db.getLanguage(chatId=call.message.chat.id)),
                         reply_markup=mk.toShop(db.getLanguage(call.message.chat.id)), parse_mode="MARKDOWN")
        # профиль меню

    if call.data == "changeLanguage":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=mk.textOfChangingLanguage(language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.switchLanguageProfile, parse_mode='MARKDOWN')

    if call.data == "profileEN" or call.data == "profileRU":
        db.setLanguage(chatId=call.message.chat.id, language="RU" if call.data == "profileRU" else "EN")

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=mk.getInfoProfile(language=db.getLanguage(call.message.chat.id),
                                                     address=db.getAddress(call.message.chat.id),
                                                     comment=db.getComment(call.message.chat.id)),
                              reply_markup=mk.profileMenu(db.getLanguage(call.message.chat.id)),
                              parse_mode='MARKDOWN')

    if call.data == "changeAddress":
        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.askLocation(db.getLanguage(chatId=call.message.chat.id)),
                         reply_markup=mk.menuLocation(db.getLanguage(chatId=call.message.chat.id)),
                         parse_mode='MARKDOWN')

    if call.data.split('#')[0] == 'listProduct':
        update_catalog_page(call.message, int(call.data.split('#')[1]))

    if call.data == "backToProfile":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.getInfoProfile(language=db.getLanguage(call.message.chat.id),
                                                     address=db.getAddress(call.message.chat.id),
                                                     comment=db.getComment(call.message.chat.id)),
                              reply_markup=mk.profileMenu(db.getLanguage(call.message.chat.id)),
                              parse_mode='MARKDOWN')

    if call.data == "toShop":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.textShop(db.getLanguage(call.message.chat.id),
                                               pm.getProducts()),
                              reply_markup=mk.sliderShop(len(pm.getProducts()) // 2,
                                                         pm.getProducts(),
                                                         db.getLanguage(call.message.chat.id)),
                              parse_mode='MARKDOWN')

    if call.data.split('#')[0] == 'productName':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        id = call.data.split('#')[1]
        send_product_page(call.message, 5, id)

    if call.data.split('#')[0] == 'coast':
        # bot.delete_message(call.message.chat.id, call.message.message_id)
        name = call.data.split('#')[1]
        page = call.data.split('#')[2]
        update_product_page(call.message, int(page), name)

    if call.data == "toShopFromVideo":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.textShop(db.getLanguage(call.message.chat.id),
                                          pm.getProducts()),
                         reply_markup=mk.sliderShop(len(pm.getProducts()) // 2,
                                                    pm.getProducts(),
                                                    db.getLanguage(call.message.chat.id)),
                         parse_mode='MARKDOWN')

    if call.data.split('#')[0] == 'toCart':
        id = call.data.split('#')[1]

        cart.addToCart(call.message.chat.id,
                       nameOfProduct=pm.getName(id),
                       numOfProducts=call.data.split('#')[2],
                       idFromProduct=id)

        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text=mk.infoCart(cart.getOfNumberOfProducts(call.message.chat.id),
                                                   db.getLanguage(call.message.chat.id)))

    if call.data == "bin":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.textTrash(products=cart.getCart(call.message.chat.id),
                                                language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.trashMenu(products=cart.getCart(call.message.chat.id),
                                                        language=db.getLanguage(call.message.chat.id)))

    if call.data == "toClearBinWarning":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.areYouSureText(language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.areYouSureMenu(language=db.getLanguage(call.message.chat.id)))

    if call.data == "toClearBin":
        cart.delProductsFromCart(call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.textTrash(products=cart.getCart(call.message.chat.id),
                                                language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.trashMenu(products=cart.getCart(call.message.chat.id),
                                                        language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'toDeliver':
        # bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.beforeOrderText(db.getAddress(call.message.chat.id),
                                                      db.getComment(call.message.chat.id),
                                                      db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.beforeOrderMenu(db.getAddress(call.message.chat.id),
                                                              db.getLanguage(call.message.chat.id),
                                                              call.data.split('#')[1]))

    if call.data.split('#')[0] == 'toConfirm':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.chooseMethodPayText(db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.chooseMethodPayMenu(call.data.split('#')[1],
                                                                  db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'forCash':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.infoOrderText(products=cart.getCart(call.message.chat.id),
                                                    fullsum=call.data.split('#')[1],
                                                    address=db.getAddress(call.message.chat.id),
                                                    comment=db.getComment(call.message.chat.id),
                                                    payment=call.data.split('#')[0],
                                                    language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.infoOrderMenu(
                                  fullprice=call.data.split('#')[1],
                                  payment=call.data.split('#')[0],
                                  language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'orderConfirm':
        numberOfOrder = ao.addActiveOrder(customer_id=call.message.chat.id,
                                          fullprice=call.data.split('#')[1],
                                          methodpay=call.data.split('#')[2],
                                          address=db.getAddress(call.message.chat.id),
                                          comment=db.getComment(call.message.chat.id))

        page = 0

        for i in ao.getAllActiveOrders():
            if ao.getActiveOrder(numberOfOrder).id == i.id:
                break
            page += 1

        for admin in am.getAdmins():
            bot.send_message(chat_id=admin.chatId,
                             text=mk.showNewActiveOrderText(numberOfOrder),
                             reply_markup=mk.showNewActiveOrderMenu(page))

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.confirmedOrderText(numberOfOrder=numberOfOrder,
                                                         language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.confirmedOrderMenu(numberOfOrder=numberOfOrder,
                                                                 language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'myOrders':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.textOrder(active=ao.getActiveOrders(call.message.chat.id),
                                                refusal=ro.getRefusalOrder(call.message.chat.id),
                                                complete=co.getCompleteOrder(call.message.chat.id),
                                                language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.sliderOrder(page=1,
                                                          active=ao.getActiveOrders(call.message.chat.id),
                                                          refusal=ro.getRefusalOrder(call.message.chat.id),
                                                          complete=co.getCompleteOrder(call.message.chat.id),
                                                          language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'order':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.textOrder(active=ao.getActiveOrders(call.message.chat.id),
                                                refusal=ro.getRefusalOrders(call.message.chat.id),
                                                complete=co.getCompleteOrders(call.message.chat.id),
                                                language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.sliderOrder(page=int(call.data.split('#')[1]),
                                                          active=ao.getActiveOrders(call.message.chat.id),
                                                          refusal=ro.getRefusalOrder(call.message.chat.id),
                                                          complete=co.getCompleteOrder(call.message.chat.id),
                                                          language=db.getLanguage(call.message.chat.id)))
    if call.data.split('#')[0] == 'lookActive':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.showActiveOrderText(activeOrders=ao.getActiveOrders(call.message.chat.id),
                                                          choosedOrder=int(call.data.split('#')[1]),
                                                          language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.showActiveOrderMenu(activeOrders=ao.getActiveOrders(call.message.chat.id),
                                                                  choosedOrder=int(call.data.split('#')[1]),
                                                                  language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'toCurrentOrder':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.showActiveOrderText(
                                  activeOrders=[ao.getActiveOrder(int(call.data.split('#')[1]))],
                                  choosedOrder=0,
                                  language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.showActiveOrderMenu(
                                  activeOrders=[ao.getActiveOrder(int(call.data.split('#')[1]))],
                                  choosedOrder=0,
                                  language=db.getLanguage(call.message.chat.id)
                              ))

    if call.data.split('#')[0] == 'lookComplete':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.showCompleteOrderText(completeOrders=co.getCompleteOrders(call.message.chat.id),
                                                            choosedOrder=int(call.data.split('#')[1]),
                                                            language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.showCompleteOrderMenu(language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'lookRefusal':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.showRefusalOrderText(refusalOrders=ro.getRefusalOrders(call.message.chat.id),
                                                           choosedOrder=int(call.data.split('#')[1]),
                                                           language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.showCompleteOrderMenu(language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'toEdit':
        id = int(call.data.split('#')[1])
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.textBinProduct(db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.sliderChangeBin(
                                  page=cart.getProductFromCart(id=id).numOfProducts,
                                  product=cart.getProductFromCart(id=id),
                                  language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'binslide':
        id = int(call.data.split('#')[1])
        page = int(call.data.split('#')[2])
        cart.changeNumOfProducts(id, page)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.textBinProduct(db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.sliderChangeBin(
                                  page=page,
                                  product=cart.getProductFromCart(id=id),
                                  language=db.getLanguage(call.message.chat.id)))

    if call.data.split('#')[0] == 'DeleteFromBin':
        id = int(call.data.split('#')[1])
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text=mk.deletedItemText(name=cart.getProductFromCart(id=id).nameOfProduct,
                                                          language=db.getLanguage(call.message.chat.id)))
        cart.delProductFromCart(id=id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.textTrash(products=cart.getCart(call.message.chat.id),
                                                language=db.getLanguage(call.message.chat.id)),
                              reply_markup=mk.trashMenu(products=cart.getCart(call.message.chat.id),
                                                        language=db.getLanguage(call.message.chat.id)))

        # админка

    if call.data == 'toMainAdmin':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.helloBoss(),
                              reply_markup=mk.helloMenu())


    if call.data == "adminOrders":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.chooseListOrdersText,
                              reply_markup=mk.chooseListOrdersMenu())

    if call.data == "activeList":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.AdminTextOrderActive(ao.getAllActiveOrders()),
                              reply_markup=mk.adminSliderOrderActive(1, ao.getAllActiveOrders()))

    if call.data.split('#')[0] == 'adminActiveOrder':
        page = int(call.data.split('#')[1])
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.AdminTextOrderActive(ao.getAllActiveOrders()),
                              reply_markup=mk.adminSliderOrderActive(page, ao.getAllActiveOrders()))

    if call.data.split('#')[0] == 'adminLookActive':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminActiveInfoText(ao.getAllActiveOrders(),
                                                          int(call.data.split('#')[1])),
                              reply_markup=mk.adminActiveInfoMenu(ao.getAllActiveOrders(),
                                                                  int(call.data.split('#')[1])))

    if call.data.split('#')[0] == 'acceptingActive':

        idOrder = int(call.data.split('#')[1])
        idCustomer = ao.getActiveOrder(idOrder).customer_id
        bot.send_message(chat_id=idCustomer,
                         text=mk.infoAccept(idOrder=idOrder,
                                            language=db.getLanguage(idCustomer)))

        ao.switchStatus(idOrder)
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text=mk.switchStatusText())

        page = 0

        for i in ao.getAllActiveOrders():
            if ao.getActiveOrder(idOrder).id == i.id:
                break
            page += 1

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminActiveInfoText(ao.getAllActiveOrders(),
                                                          page),
                              reply_markup=mk.adminActiveInfoMenu(ao.getAllActiveOrders(), page))

    if call.data.split('#')[0] == 'completingActive':
        id = int(call.data.split('#')[1])
        co.switcherActiveToComplete(ao.getActiveOrder(id))
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.switchActiveToCompleteText(id),
                              reply_markup=mk.switchActiveToCompleteMenu())

    if call.data.split('#')[0] == 'refusingActive':
        idActive = int(call.data.split('#')[1])
        page = int(call.data.split('#')[2])
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=mk.switchActiveToRefusalText(
                                        db.getLanguage(ao.getActiveOrder(idActive).customer_id)),
                                    reply_markup=mk.switchActiveToRefusalMenu(page))
        bot.register_next_step_handler(msg, toWriteReasonForRefusal, idActive, call.message.message_id)

    if call.data.split('#')[0] == 'activeToRefusalCancel':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminActiveInfoText(ao.getAllActiveOrders(),
                                                          int(call.data.split('#')[1])),
                              reply_markup=mk.adminActiveInfoMenu(ao.getAllActiveOrders(),
                                                                  int(call.data.split('#')[1])))

    if call.data.split('#')[0] == 'messageToCustomer':

        idCustomer = int(call.data.split('#')[1])
        idOrder = int(call.data.split('#')[2])

        if len(list(call.data.split('#'))) == 4:

            page = int(call.data.split('#')[3])
            msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=mk.toCommunicateWithCustomerText(idOrder),
                                        reply_markup=mk.toCommunicateWithCustomerMenu(page))

            bot.register_next_step_handler(msg, toCommunicateAdminToCustomerFromOrders, idCustomer,
                                           idOrder, call.message.message_id, page)

        elif len(list(call.data.split('#'))) == 3:

            page = 0

            for i in ao.getAllActiveOrders():
                if ao.getActiveOrder(idOrder).id == i.id:
                    break
                page += 1

            msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=mk.toCommunicateWithCustomerText(idOrder),
                                        reply_markup=mk.toAnswerToCustomerMenu(page))

            bot.register_next_step_handler(msg, toCommunicateAdminToCustomerFromOrders, idCustomer,
                                           idOrder, call.message.message_id, page)



    if call.data.split('#')[0] == 'adminCommunicateCancel':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminActiveInfoText(ao.getAllActiveOrders(),
                                                          int(call.data.split('#')[1])),
                              reply_markup=mk.adminActiveInfoMenu(ao.getAllActiveOrders(),
                                                                  int(call.data.split('#')[1])))

    if call.data == 'answerToAdminCancel':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.message_id)


    if call.data.split('#')[0] == 'toAnswerToAdmin':
        idAdmin = call.data.split('#')[1]
        idOrder = call.data.split('#')[2]

        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=mk.toAnswerToAdminText(db.getLanguage(call.message.chat.id)),
                                    reply_markup=mk.toAnswerToAdminMenu(db.getLanguage(call.message.chat.id)))
        bot.register_next_step_handler(msg, toAnswerToAdminStepper, idAdmin, idOrder, call.message.message_id)


    if call.data.split('#')[0] == "toWriteCourier":

        idOrder = int(call.data.split('#')[1])

        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=mk.toAnswerToAdminText(db.getLanguage(call.message.chat.id)),
                                    reply_markup=mk.toAnswerToAdminMenu(db.getLanguage(call.message.chat.id)))

        bot.register_next_step_handler(msg, toWriteToAdminStepper, idOrder, call.message.message_id)

    if call.data == "refusalList":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.AdminTextOrderRefusal(ro.getAllRefusalOrders()),
                              reply_markup=mk.adminSliderOrderRefusal(1, ro.getAllRefusalOrders()))

    if call.data.split('#')[0] == 'adminRefusalOrder':
        page = int(call.data.split('#')[1])
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.AdminTextOrderRefusal(ro.getAllRefusalOrders()),
                              reply_markup=mk.adminSliderOrderRefusal(page, ro.getAllRefusalOrders()))

    if call.data.split('#')[0] == 'adminLookRefusal':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminRefusalInfoText(ro.getAllRefusalOrders(),
                                                          int(call.data.split('#')[1])),
                              reply_markup=mk.adminRefusalInfoMenu())

    if call.data == "completeList":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.AdminTextOrderComplete(co.getAllCompleteOrders()),
                              reply_markup=mk.adminSliderOrderComplete(1, co.getAllCompleteOrders()))

    if call.data.split('#')[0] == 'adminCompleteOrder':
        page = int(call.data.split('#')[1])
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.AdminTextOrderComplete(co.getAllCompleteOrders()),
                              reply_markup=mk.adminSliderOrderComplete(page, co.getAllCompleteOrders()))

    if call.data.split('#')[0] == 'adminLookComplete':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminCompleteInfoText(co.getAllCompleteOrders(),
                                                            int(call.data.split('#')[1])),
                              reply_markup=mk.adminCompleteInfoMenu())

    if call.data == 'adminPostSale':
        post.delPost(call.message.chat.id)
        post.addToPost(call.message.chat.id)
        adminPostSaleChecker[call.message.chat.id] = True
        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=mk.adminBeforePostTextRU(),
                                    reply_markup=mk.adminBeforePostMenu())

        bot.register_next_step_handler(msg, toPostAdminTextRU)


    if call.data == 'attachVideo':
        post.setDirType(call.message.chat.id, "video")
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminPostToAttachVideo(),
                              reply_markup=mk.adminBeforePostMenu())

    if call.data == 'attachPhoto':
        post.setDirType(call.message.chat.id, "photo")
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminPostToAttachPhoto(),
                              reply_markup=mk.adminBeforePostMenu())

    if call.data == 'noAttach':
        users = db.getAllCustomers()
        newPost = post.getPost(call.message.chat.id)

        for user in users:

            if user.language == "RU":
                bot.send_message(chat_id=user.chatId,
                                 text=newPost.textRU)

            elif user.language == "EN":
                bot.send_message(chat_id=user.chatId,
                                 text=newPost.textEN)
        post.delPost(call.message.chat.id)
        adminPostSaleChecker[call.message.chat.id] = False
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.helloBoss(),
                         reply_markup=mk.helloMenu())



    if call.data == 'resetPost':

        bot.clear_step_handler_by_chat_id(call.message.chat.id)

        adminPostSaleChecker[call.message.chat.id] = False

        if post.getPost(call.message.chat.id).dirMedia is not None:
            os.remove(post.getPost(call.message.chat.id).dirMedia)

        post.delPost(call.message.chat.id)

        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)

        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.helloBoss(),
                         reply_markup=mk.helloMenu())

    if call.data == 'adminToPublishPost':

        users = db.getAllCustomers()
        newPost = post.getPost(call.message.chat.id)

        if newPost.dirType == "video":

            for user in users:

                if user.language == "RU":
                    bot.send_video(chat_id=user.chatId,
                                   video=open(newPost.dirMedia, 'rb'),
                                   caption=newPost.textRU)

                elif user.language == "EN":
                    bot.send_video(chat_id=user.chatId,
                                   video=open(newPost.dirMedia, 'rb'),
                                   caption=newPost.textEN)

        elif newPost.dirType == "photo":

            for user in users:

                if user.language == "RU":
                    bot.send_photo(chat_id=user.chatId,
                                   photo=open(newPost.dirMedia, 'rb'),
                                   caption=newPost.textRU)

                elif user.language == "EN":
                    bot.send_photo(chat_id=user.chatId,
                                   photo=open(newPost.dirMedia, 'rb'),
                                   caption=newPost.textEN)
        os.remove(newPost.dirMedia)
        post.delPost(call.message.chat.id)
        adminPostSaleChecker[call.message.chat.id] = False
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.helloBoss(),
                         reply_markup=mk.helloMenu())

    if call.data == 'adminCatalog':

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminListProductText(pm.getProducts()),
                              reply_markup=mk.adminSliderShop(1, pm.getProducts()))

    if call.data.split('#')[0] == 'adminListProduct':

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminListProductText(pm.getProducts()),
                              reply_markup=mk.adminSliderShop(int(call.data.split('#')[1]), pm.getProducts()))

    if call.data.split('#')[0] == 'adminProductName':
        idProduct = int(call.data.split('#')[1])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        product = pm.getProduct(idProduct)

        if product.typeMedia == "video":

            bot.send_video(chat_id=call.message.chat.id,
                           video=open(product.dirMedia, 'rb'),
                           caption=mk.adminTextProduct(product),
                           reply_markup=mk.adminProductMenu(idProduct))

        elif product.typeMedia == "photo":

            bot.send_photo(chat_id=call.message.chat.id,
                           photo=open(product.dirMedia, 'rb'),
                           caption=mk.adminTextProduct(product),
                           reply_markup=mk.adminProductMenu(idProduct))

    if call.data == "adminCatalogFromMedia":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.adminListProductText(pm.getProducts()),
                         reply_markup=mk.adminSliderShop(1, pm.getProducts()))

    if call.data.split('#')[0] == "adminDeleteProduct":
        idProduct = int(call.data.split('#')[1])
        os.remove(pm.getMedia(idProduct))
        pm.delProduct(idProduct)

        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text=mk.delProductText())

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.adminListProductText(pm.getProducts()),
                         reply_markup=mk.adminSliderShop(1, pm.getProducts()))

    if call.data == "adminAddProduct":
        npm.delNewProd(call.message.chat.id)
        npm.addNewProduct(call.message.chat.id)
        adminAddProductChecker[call.message.chat.id] = True


        msg = bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=mk.adminAddProductName(),
                                    reply_markup=mk.adminAddProductNameMenu())

        bot.register_next_step_handler(msg, toNewProdName)

    if call.data == "attachVideoToProduct":
        npm.setType(call.message.chat.id, "video")
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminPostToAttachVideo(),
                              reply_markup=mk.adminAddProductNameMenu())

    if call.data == "attachPhotoToProduct":
        npm.setType(call.message.chat.id, "photo")
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=mk.adminPostToAttachPhoto(),
                              reply_markup=mk.adminAddProductNameMenu())

    if call.data == 'resetProduct':

        bot.clear_step_handler_by_chat_id(call.message.chat.id)

        adminAddProductChecker[call.message.chat.id] = False

        if npm.getNewProd(call.message.chat.id).dirMedia is not None:
            os.remove(npm.getNewProd(call.message.chat.id).dirMedia)

        npm.delNewProd(call.message.chat.id)

        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)

        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.adminListProductText(pm.getProducts()),
                         reply_markup=mk.adminSliderShop(1, pm.getProducts()))

    if call.data == 'addProductInFinish':
        pm.switcherNewProductToFinishProduct(npm.getNewProd(call.message.chat.id))
        adminAddProductChecker[call.message.chat.id] = False

        users = db.getAllCustomers()

        for user in users:
            bot.send_message(chat_id=user.chatId,
                             text=mk.feedbackNewPost(user.language))

        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text=mk.feedbackAdminNewPost())

        bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.adminListProductText(pm.getProducts()),
                         reply_markup=mk.adminSliderShop(1, pm.getProducts()))

    if call.data == 'addProductInStart':
        pm.switcherNewProductToStartProduct(npm.getNewProd(call.message.chat.id))
        adminAddProductChecker[call.message.chat.id] = False

        users = db.getAllCustomers()

        for user in users:
            bot.send_message(chat_id=user.chatId,
                             text=mk.feedbackNewPost(user.language))

        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=True,
                                  text=mk.feedbackAdminNewPost())

        bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.send_message(chat_id=call.message.chat.id,
                         text=mk.adminListProductText(pm.getProducts()),
                         reply_markup=mk.adminSliderShop(1, pm.getProducts()))

    if call.data.split('#')[0] == 'adminChangeName':
        idProduct = int(call.data.split('#')[1])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        msg = bot.send_message(chat_id=call.message.chat.id,
                               text=mk.adminAddProductName(),
                               reply_markup=mk.adminChangeMenu(idProduct))
        bot.register_next_step_handler(msg, toWriteNameChangingProduct, idProduct)

    if call.data.split('#')[0] == 'adminChangeInfoAbout':
        idProduct = int(call.data.split('#')[1])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        msg = bot.send_message(chat_id=call.message.chat.id,
                               text=mk.adminAddProductText(),
                               reply_markup=mk.adminChangeMenu(idProduct))
        bot.register_next_step_handler(msg, toWriteInfoAboutChangingProduct, idProduct)

    if call.data.split('#')[0] == 'adminChangePrice':
        idProduct = int(call.data.split('#')[1])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        msg = bot.send_message(chat_id=call.message.chat.id,
                               text=mk.adminAddProductPrice(),
                               reply_markup=mk.adminChangeMenu(idProduct))
        bot.register_next_step_handler(msg, toWritePriceChangingProduct, idProduct)

    if call.data.split('#')[0] == 'resetChanging':
        idProduct = int(call.data.split('#')[1])

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.clear_step_handler_by_chat_id(call.message.chat.id)

        product = pm.getProduct(idProduct)

        if product.typeMedia == "video":

            bot.send_video(chat_id=call.message.chat.id,
                           video=open(product.dirMedia, 'rb'),
                           caption=mk.adminTextProduct(product),
                           reply_markup=mk.adminProductMenu(idProduct))

        elif product.typeMedia == "photo":

            bot.send_photo(chat_id=call.message.chat.id,
                           photo=open(product.dirMedia, 'rb'),
                           caption=mk.adminTextProduct(product),
                           reply_markup=mk.adminProductMenu(idProduct))


def toWritePriceChangingProduct(message, idProduct):
    pm.setPrice(idProduct, message.text)

    product = pm.getProduct(idProduct)

    if product.typeMedia == "video":

        bot.send_video(chat_id=message.chat.id,
                       video=open(product.dirMedia, 'rb'),
                       caption=mk.adminTextProduct(product),
                       reply_markup=mk.adminProductMenu(idProduct))

    elif product.typeMedia == "photo":

        bot.send_photo(chat_id=message.chat.id,
                       photo=open(product.dirMedia, 'rb'),
                       caption=mk.adminTextProduct(product),
                       reply_markup=mk.adminProductMenu(idProduct))
def toWriteInfoAboutChangingProduct(message, idProduct):
    pm.setInfoAbout(idProduct, message.text)

    product = pm.getProduct(idProduct)

    if product.typeMedia == "video":

        bot.send_video(chat_id=message.chat.id,
                       video=open(product.dirMedia, 'rb'),
                       caption=mk.adminTextProduct(product),
                       reply_markup=mk.adminProductMenu(idProduct))

    elif product.typeMedia == "photo":

        bot.send_photo(chat_id=message.chat.id,
                       photo=open(product.dirMedia, 'rb'),
                       caption=mk.adminTextProduct(product),
                       reply_markup=mk.adminProductMenu(idProduct))
def toWriteNameChangingProduct(message, idProduct):
    pm.setName(idProduct, message.text)

    product = pm.getProduct(idProduct)

    if product.typeMedia == "video":

        bot.send_video(chat_id=message.chat.id,
                       video=open(product.dirMedia, 'rb'),
                       caption=mk.adminTextProduct(product),
                       reply_markup=mk.adminProductMenu(idProduct))

    elif product.typeMedia == "photo":

        bot.send_photo(chat_id=message.chat.id,
                       photo=open(product.dirMedia, 'rb'),
                       caption=mk.adminTextProduct(product),
                       reply_markup=mk.adminProductMenu(idProduct))

def toNewProdName(message):
    npm.setName(message.chat.id, message.text)

    msg = bot.send_message(chat_id=message.chat.id,
                           text=mk.adminAddProductText(),
                           reply_markup=mk.adminAddProductNameMenu())

    bot.register_next_step_handler(msg, toNewProdText)

def toNewProdText(message):
    npm.setInfoAbout(message.chat.id, message.text)

    msg = bot.send_message(chat_id=message.chat.id,
                           text=mk.adminAddProductPrice(),
                           reply_markup=mk.adminAddProductNameMenu())

    bot.register_next_step_handler(msg, toNewProdPrice)
def toNewProdPrice(message):
    npm.setPrice(message.chat.id, message.text)

    bot.send_message(chat_id=message.chat.id,
                     text=mk.adminAddProductMediaText(npm.getNewProd(message.chat.id)),
                     reply_markup=mk.adminAddProductMediaMenu())

def toPostAdminTextRU(message):

    post.setTextRU(message.chat.id, message.text)

    msg = bot.send_message(chat_id=message.chat.id,
                           text=mk.adminBeforePostTextEN(),
                           reply_markup=mk.adminBeforePostMenu())

    bot.register_next_step_handler(msg, toPostAdminTextEN)

def toPostAdminTextEN(message):

    post.setTextEN(message.chat.id, message.text)

    bot.send_message(chat_id=message.chat.id,
                     text=mk.adminGetTypePostText(post.getPost(message.chat.id).textRU,
                                                  post.getPost(message.chat.id).textEN),
                     reply_markup=mk.adminGetTypePostMenu())
def toWriteToAdminStepper(message, idOrder, messageToDelete):
    bot.delete_message(message.chat.id, messageToDelete)

    for admin in am.getAdmins():
        bot.send_message(chat_id=admin.chatId,
                         text=mk.sendingToAdminText(idOrder, message.text),
                         reply_markup=mk.sendingToAdminMenu(idOrder, message.chat.id))

    bot.send_message(chat_id=message.chat.id,
                     text=mk.feedbackToCustomerAfterSendAdminText(db.getLanguage(message.chat.id)))
def toAnswerToAdminStepper(message, idAdmin, idOrder, messageToDelete):
    bot.delete_message(message.chat.id, messageToDelete)

    bot.send_message(chat_id=idAdmin,
                     text=mk.sendingToAdminText(idOrder, message.text),
                     reply_markup=mk.sendingToAdminMenu(idOrder, message.chat.id))

    bot.send_message(chat_id=message.chat.id,
                     text=mk.feedbackToCustomerAfterSendAdminText(db.getLanguage(message.chat.id)))
def toCommunicateAdminToCustomerFromOrders(message, idCustomer, idOrder, messageToDelete, page):
    bot.delete_message(message.chat.id, messageToDelete)

    bot.send_message(chat_id=idCustomer,
                     text=mk.sendingToCustomerText(idOrder, message.text, db.getLanguage(idCustomer)),
                     reply_markup=mk.sendingToCustomerMenu(idOrder, message.chat.id, db.getLanguage(idCustomer)))

    bot.send_message(chat_id=message.chat.id,
                     text=mk.answerNextSendToCustomerText(idOrder),
                     reply_markup=mk.answerNextSendToCustomerMenu(page))


def toWriteReasonForRefusal(message, idActive, messageToDelete):

    bot.delete_message(message.chat.id, messageToDelete)
    idCustomer = ao.getActiveOrder(idActive).customer_id
    bot.send_message(chat_id=idCustomer,
                     text=mk.infoReason(idOrder=idActive, text=message.text, language=db.getLanguage(idCustomer)))

    ro.switcherActiveToRefusal(ao.getActiveOrder(idActive), message.text)

    bot.send_message(chat_id=message.chat.id,
                     text=mk.infoActiveToRefusalText(idActive),
                     reply_markup=mk.infoActiveToRefusalMenu())


def update_catalog_page(message, page):
    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=mk.textShop(db.getLanguage(message.chat.id),
                             pm.getProducts()),
            reply_markup=mk.sliderShop(page, pm.getProducts(), db.getLanguage(message.chat.id)),
            parse_mode='MARKDOWN'
        )

    except ApiTelegramException:
        pass


def send_product_page(message, page, idProduct):

    product = pm.getProduct(idProduct)
    if product.typeMedia == "video":
        bot.send_video(chat_id=message.chat.id,
                       video=open(pm.getMedia(idProduct), 'rb'),
                       caption=mk.textProduct(name=pm.getName(idProduct),
                                              infoAbout=pm.getInfoAbout(idProduct),
                                              price=pm.getPrice(idProduct),
                                              language=db.getLanguage(message.chat.id)),
                       reply_markup=mk.sliderProduct(page, idProduct,
                                                     pm.getPrice(idProduct),
                                                     db.getLanguage(message.chat.id)),
                       parse_mode='MARKDOWN')

    if product.typeMedia == "photo":
        bot.send_photo(chat_id=message.chat.id,
                       photo=open(pm.getMedia(idProduct), 'rb'),
                       caption=mk.textProduct(name=pm.getName(idProduct),
                                              infoAbout=pm.getInfoAbout(idProduct),
                                              price=pm.getPrice(idProduct),
                                              language=db.getLanguage(message.chat.id)),
                       reply_markup=mk.sliderProduct(page, idProduct,
                                                     pm.getPrice(idProduct),
                                                     db.getLanguage(message.chat.id)),
                       parse_mode='MARKDOWN')

def update_product_page(message, page, id):
    try:
        bot.edit_message_caption(chat_id=message.chat.id,
                                 message_id=message.message_id,
                                 caption=mk.textProduct(name=pm.getName(id),
                                                        infoAbout=pm.getInfoAbout(id),
                                                        price=pm.getPrice(id),
                                                        language=db.getLanguage(message.chat.id)),
                                 reply_markup=mk.sliderProduct(page, id,
                                                               pm.getPrice(id),
                                                               db.getLanguage(message.chat.id)),
                                 parse_mode='MARKDOWN')

    except ApiTelegramException:
        pass

@bot.message_handler(content_types=['photo', 'video'])
def handler_file(message):

    if am.checkAdmin(chatId=message.chat.id):

        if adminPostSaleChecker.get(message.chat.id):

            if message.content_type == 'photo' and post.getPost(message.chat.id).dirType == "photo":

                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                print(file_info.file_unique_id)

                src = f'{pathlib.Path.cwd()}/../attachments/{file_info.file_unique_id}.jpg'

                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                post.setDirMedia(message.chat.id, src)

                bot.send_photo(chat_id=message.chat.id,
                               photo=open(post.getPost(message.chat.id).dirMedia, 'rb'),
                               caption=mk.adminFinalPostText(textRU=post.getPost(message.chat.id).textRU,
                                                             textEN=post.getPost(message.chat.id).textEN),
                               reply_markup=mk.adminFinalPostMenu(),
                               parse_mode='MARKDOWN')

            if message.content_type == 'video' and post.getPost(message.chat.id).dirType == "video":

                file_info = bot.get_file(message.video.file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = f'{pathlib.Path.cwd()}/../attachments/{file_info.file_unique_id}.mp4'

                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                post.setDirMedia(message.chat.id, src)

                bot.send_video(chat_id=message.chat.id,
                               video=open(post.getPost(message.chat.id).dirMedia, 'rb'),
                               caption=mk.adminFinalPostText(textRU=post.getPost(message.chat.id).textRU,
                                                             textEN=post.getPost(message.chat.id).textEN),
                               reply_markup=mk.adminFinalPostMenu(),
                               parse_mode='MARKDOWN')

        elif adminAddProductChecker.get(message.chat.id):

            if message.content_type == 'photo' and npm.getNewProd(message.chat.id).typeMedia == "photo":

                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                print(file_info.file_unique_id)

                src = f'{pathlib.Path.cwd()}/../files/{file_info.file_unique_id}.jpg'

                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                npm.setDirMedia(message.chat.id, src)

                bot.send_photo(chat_id=message.chat.id,
                               photo=open(npm.getNewProd(message.chat.id).dirMedia, 'rb'),
                               caption=mk.adminAddProductMediaText(npm.getNewProd(message.chat.id)),
                               reply_markup=mk.adminFinalProductMenu(),
                               parse_mode='MARKDOWN')

            if message.content_type == 'video' and npm.getNewProd(message.chat.id).typeMedia == "video":

                file_info = bot.get_file(message.video.file_id)
                downloaded_file = bot.download_file(file_info.file_path)

                src = f'{pathlib.Path.cwd()}/../files/{file_info.file_unique_id}.mp4'

                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                npm.setDirMedia(message.chat.id, src)

                bot.send_video(chat_id=message.chat.id,
                               video=open(npm.getNewProd(message.chat.id).dirMedia, 'rb'),
                               caption=mk.adminAddProductMediaText(npm.getNewProd(message.chat.id)),
                               reply_markup=mk.adminFinalProductMenu(),
                               parse_mode='MARKDOWN')
@bot.message_handler(content_types=['location'])
def getLocation(message):
    print(message.location.latitude, message.location.longitude)
    db.setAddress(chatId=message.chat.id, location=get_address(lat=message.location.latitude,
                                                               lon=message.location.longitude,
                                                               language=db.getLanguage(message.chat.id)))
    db.setComment(chatId=message.chat.id, comment=None)
    msg = bot.send_message(chat_id=message.chat.id,
                           text=mk.addressInfo(db.getLanguage(chatId=message.chat.id),
                                               db.getAddress(chatId=message.chat.id))
                                + "\n\n" + mk.toCommentAddress(db.getLanguage(chatId=message.chat.id)),
                           reply_markup=mk.toCommentAdress(db.getLanguage(chatId=message.chat.id)),
                           parse_mode='MARKDOWN')

    bot.register_next_step_handler(msg, stepByGetAddress)


if __name__ == '__main__':
    bot.infinity_polling()
