from telebot import types
from telegram_bot_pagination import InlineKeyboardPaginator
from app.models import ProductModel as pm
from app.models import CustomerModel as db
from app.models import ActiveOrderModel as ao
hideMenu = types.ReplyKeyboardRemove()

# до меню профиль-купить

toBuyMarkupRU = "Купить"
toProfileMarkupRU = "Профиль"
toBuyMarkupEN = "Buy"
toProfileMarkupEN = "Profile"

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


def welcomeText(language: str):
    if language == "RU":
        return '''Привет!
Ты в крутом магазине на крутом острове
Можешь сделать заказ и оформить доставку'''

    if language == "EN":
        return '''Hello!
You are in the cool boshkiShop on cool Island
You can make an order and do delivery'''


def askLocation(language: str):
    if language == "RU":
        return "Напишите свой адрес или отправьте свою геолокацию"

    if language == "EN":
        return "Write your address or send geolocation"


sendLocationRU = types.KeyboardButton("Отправить геолокацию", request_location=True)
writeLocationRU = types.KeyboardButton("Написать адрес текстом")
passLocationRU = types.KeyboardButton("Пропустить сейчас")
sendLocationEN = types.KeyboardButton("Send location", request_location=True)
writeLocationEN = types.KeyboardButton("Write the address in text")
passLocationEN = types.KeyboardButton("Pass now")


def menuLocation(language: str):
    menuLocation = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)

    if language == "RU":

        return menuLocation.add(sendLocationRU, writeLocationRU, passLocationRU)

    elif language == "EN":

        return menuLocation.add(sendLocationEN, writeLocationEN, passLocationEN)


def menuBuyProfile(language: str):
    menuBuyProfile = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    if language == "RU":
        toBuyRU = types.KeyboardButton(toBuyMarkupRU)
        toProfileRU = types.KeyboardButton(toProfileMarkupRU)
        return menuBuyProfile.add(toBuyRU, toProfileRU)

    elif language == "EN":
        toBuyEN = types.KeyboardButton(toBuyMarkupEN)
        toProfileEN = types.KeyboardButton(toProfileMarkupEN)
        return menuBuyProfile.add(toBuyEN, toProfileEN)


passCommentRU = types.InlineKeyboardButton("Пропустить", callback_data="passCommentAdress")
# toBackRU = types.InlineKeyboardButton("Назад", callback_data="toBackFromCommentAdress")
passCommentEN = types.InlineKeyboardButton("Pass", callback_data="passCommentAdress")


# toBackEN = types.InlineKeyboardButton("To back", callback_data="toBackFromCommentAdress")

def toCommentAdress(language: str):
    toCommentAdress = types.InlineKeyboardMarkup(row_width=1)

    if language == "RU":

        return toCommentAdress.add(passCommentRU)

    elif language == "EN":

        return toCommentAdress.add(passCommentEN)


def addressInfo(language: str, address: str):
    if language == "RU":
        return f'Адрес: {address}\nЕсли он неверный, измените его в профиле'

    elif language == "EN":
        return f'Address: {address}\nIf it incorrect, change one in profile'


def toCommentAddress(language: str):
    if language == "RU":
        return 'Укажите комментарий к адресу:'
    elif language == "EN":
        return 'Write comment for adrress:'


def inviteToWriteAddress(language: str):
    if language == "RU":
        return 'Введите ваш полный адрес и отправьте:'
    elif language == "EN":
        return 'Write your complete address and send:'


def addressAddedSuccessfully(language: str):
    if language == "RU":
        return 'Адрес успешно добавлен!\nМожешь переходить к покупкам!'
    elif language == "EN":
        return 'Address has added successfully!\nYou can go to buy!'


toShopRU = types.InlineKeyboardButton("В магазин", callback_data="toShop")
toShopEN = types.InlineKeyboardButton("To shop", callback_data="toShop")
toProfileRU = types.InlineKeyboardButton("В профиль", callback_data="backToProfile")
toProfileEN = types.InlineKeyboardButton("To profile", callback_data="backToProfile")
def toShop(language: str):
    toShop = types.InlineKeyboardMarkup(row_width=1)

    if language == "RU":
        return toShop.add(toShopRU, toProfileRU)

    elif language == "EN":
        return toShop.add(toShopEN, toProfileEN)


def indexAddreessLater(language: str):
    if language == "RU":
        return "Если понадобится, ты можешь указать адрес в профиле"

    elif language == "EN":
        return "If it'll be need, you can point address at profile"


# профиль
profileMarkup = types.InlineKeyboardMarkup(row_width=1)
profileButtonRU1 = types.InlineKeyboardButton("Изменить адрес", callback_data="changeAddress")
profileButtonRU2 = types.InlineKeyboardButton("Мои заказы", callback_data="myOrders")
profileButtonRU3 = types.InlineKeyboardButton("Корзина", callback_data="bin")
profileButtonRU4 = types.InlineKeyboardButton("Реферальная система", callback_data="refSystem")
# profileButtonRU5 = types.InlineKeyboardButton("Указать контакт", callback_data="pointContant")
profileButtonRU6 = types.InlineKeyboardButton("Изменить язык", callback_data="changeLanguage")

profileButtonEN1 = types.InlineKeyboardButton("Change address", callback_data="changeAddress")
profileButtonEN2 = types.InlineKeyboardButton("My orders", callback_data="myOrders")
profileButtonEN3 = types.InlineKeyboardButton("Bin", callback_data="bin")
profileButtonEN4 = types.InlineKeyboardButton("Ref system", callback_data="refSystem")
# profileButtonEN5 = types.InlineKeyboardButton("Point contact", callback_data="pointContant")
profileButtonEN6 = types.InlineKeyboardButton("Change language", callback_data="changeLanguage")


def profileMenu(language: str):
    profileMarkup = types.InlineKeyboardMarkup(row_width=1)
    if language == "RU":
        return profileMarkup.add(profileButtonRU1, profileButtonRU2, profileButtonRU3, profileButtonRU4,
                                 profileButtonRU6)

    elif language == "EN":
        return profileMarkup.add(profileButtonEN1, profileButtonEN2, profileButtonEN3, profileButtonEN4,
                                 profileButtonEN6)


def getInfoProfile(language: str, address: str, comment: str):
    if language == "RU":
        return f'''Профиль
Адрес: {address if address is not None else "не указан"}
Комментарий к адресу: {comment if comment is not None else "не указан"}'''

    elif language == "EN":
        return f'''Profile
Address: {address if address is not None else "didn't point"}
Comment for address: {comment if comment is not None else "didn't point"}'''


def textOfChangingLanguage(language: str):
    if language == "RU":
        return 'Выберите язык'

    elif language == "EN":
        return 'Choose language'


switchLanguageProfile = types.InlineKeyboardMarkup(row_width=1)
languageProfileEN = types.InlineKeyboardButton("English", callback_data="profileEN")
languageProfileRU = types.InlineKeyboardButton("Русский", callback_data="profileRU")
switchLanguageProfile.add(languageProfileEN, languageProfileRU)


# шоп

class sliderShopPaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = '<-'
    current_page_label = '·  {}  ·'
    next_page_label = '->'
    last_page_label = '>>'


def textShop(language, products):
    if len(products) != 0:
        if language == "RU":
            return "Список товаров\nВыберите нужный и нажмите"
        elif language == "EN":
            return "List of products\nChoose you needed and push"
    else:
        if language == "RU":
            return "Сейчас товаров нет в магазине ;("
        if language == "EN":
            return "Now at shop there aren't products"


def sliderShop(page, products, language):
    if len(products) != 0:

        nameOfProducts = list(i.name for i in products)
        idOrders = list(i.id for i in products)
        paginator = sliderShopPaginator(page_count=len(nameOfProducts),
                                        current_page=page,
                                        data_pattern='listProduct#{page}')

        lookProduct = types.InlineKeyboardButton('{}'.format(nameOfProducts[page - 1]),
                                                 callback_data='productName#{}'.format(idOrders[page - 1]))
        paginator.add_before(lookProduct)

        if language == "RU":

            toBackButton = types.InlineKeyboardButton('Назад', callback_data='backToProfile')
            paginator.add_after(toBackButton)

        elif language == "EN":

            toBackButton = types.InlineKeyboardButton('Go back', callback_data='backToProfile')
            paginator.add_after(toBackButton)

        return paginator.markup

    else:
        menuBack = types.InlineKeyboardMarkup(row_width=1)
        if language == "RU":
            toBack = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
            return menuBack.add(toBack)
        if language == "EN":
            toBack = types.InlineKeyboardButton("Back", callback_data="backToProfile")
            return menuBack.add(toBack)


class sliderProductPaginator(InlineKeyboardPaginator):
    first_page_label = ''
    previous_page_label = ' - '
    next_page_label = ' + '
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
        page_count=500,
        current_page=page,
        data_pattern='coast#' + name + '#{page}'
    )
    paginator.current_page_label = '{}' + ' | {} BATH'.format(int(page) * price)

    if language == "RU":

        # toChooseNumberOf = types.InlineKeyboardButton('Указать количество', callback_data='toChooseNumberOf')
        # toOrderDelivery = types.InlineKeyboardButton('Заказать доставку', callback_data='toOrderDelivery')
        toCart = types.InlineKeyboardButton('В корзину', callback_data='toCart#{}#{}'.format(name, int(page)))
        toBackButton = types.InlineKeyboardButton('Назад', callback_data='toShopFromVideo')
        paginator.add_before(toCart)
        paginator.add_after(toBackButton)

    elif language == "EN":

        # toChooseNumberOf = types.InlineKeyboardButton('Indicate quantity', callback_data='toChooseNumberOf')
        # toOrderDelivery = types.InlineKeyboardButton('Order delivery', callback_data='toOrderDelivery')
        toCart = types.InlineKeyboardButton('Add to cart', callback_data='toCart#{}#{}'.format(name, int(page)))
        toBackButton = types.InlineKeyboardButton('Back', callback_data='toShopFromVideo')

        paginator.add_before(toCart)
        paginator.add_after(toBackButton)

    return paginator.markup


def infoCart(num: int, language: str):
    if language == "RU":
        return "Товаров в корзине: {}\nОформи заказ через профиль".format(num)

    elif language == "EN":
        return "Items in the cart: {}\nPlace an order through your profile".format(num)


def textTrash(products, language):
    if len(products) != 0:

        if language == "RU":
            head = "Товаров в корзине: {}\n\nНажми на товар чтобы удалить или изменить".format(len(products))

            return head

        if language == "EN":
            head = "Items in the cart: {}\n\nTouch on product for delete or change".format(len(products))

            return head

    else:
        if language == "RU":
            return "Твоя корзина пуста ;("
        if language == "EN":
            return "Your trash is empty ;("


# def trashMenu(products, language):
#
#     trashMenu = types.InlineKeyboardMarkup(row_width=1)
#
#     if len(products) != 0:
#
#         totalsum = 0
#         for product in products:
#             product = str(product)
#
#             if pm.getPrice(product.split('#')[0]) != 0:
#
#                 name = product.split('#')[0]
#
#                 price = pm.getPrice(name)
#                 num = int(product.split('#')[1])
#                 sum = num * price
#                 totalsum += sum
#
#         if language == "RU":
#             toDeliver = types.InlineKeyboardButton("Заказать | {} BATH".format(totalsum), callback_data="toDeliver#{}".format(totalsum))
#             toClearBin = types.InlineKeyboardButton("Очистить корзину", callback_data="toClearBinWarning")
#             toBack = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
#             trashMenu.add(toDeliver, toClearBin, toBack)
#
#         if language == "EN":
#             toDeliver = types.InlineKeyboardButton("Order | {} BATH".format(totalsum), callback_data="toDeliver#{}".format(totalsum))
#             toClearBin = types.InlineKeyboardButton("Empty trash", callback_data="toClearBinWarning")
#             toBack = types.InlineKeyboardButton("To back", callback_data="backToProfile")
#             trashMenu.add(toDeliver, toClearBin, toBack)
#     else:
#         if language == "RU":
#             toBack = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
#             trashMenu.add(toBack)
#
#         if language == "EN":
#             toBack = types.InlineKeyboardButton("To back", callback_data="backToProfile")
#             trashMenu.add(toBack)
#
#     return trashMenu

def trashMenu(products, language):
    trashMenu = types.InlineKeyboardMarkup(row_width=1)

    if len(products) != 0:

        totalsum = 0
        i = 0
        for product in products:

            if pm.getPrice(product.idFromProduct) is not False:

                name = product.nameOfProduct

                price = pm.getPrice(product.idFromProduct)
                num = product.numOfProducts
                sum = num * price
                totalsum += sum

                if language == "RU":
                    button = types.InlineKeyboardButton(f"{name} | {str(num)} грамм | {price * num} BATH",
                                                        callback_data=f"toEdit#{product.id}")
                    trashMenu.add(button)
                if language == "EN":
                    button = types.InlineKeyboardButton(f"{name} | {str(num)} gramm | {price * num} BATH",
                                                        callback_data=f"toEdit#{product.id}")
                    trashMenu.add(button)

            i += 1

        if language == "RU":
            toDeliver = types.InlineKeyboardButton("Заказать | {} BATH".format(totalsum),
                                                   callback_data="toDeliver#{}".format(totalsum))
            toClearBin = types.InlineKeyboardButton("Очистить корзину", callback_data="toClearBinWarning")
            toBack = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
            trashMenu.add(toDeliver, toClearBin, toBack)

        if language == "EN":
            toDeliver = types.InlineKeyboardButton("Order | {} BATH".format(totalsum),
                                                   callback_data="toDeliver#{}".format(totalsum))
            toClearBin = types.InlineKeyboardButton("Empty trash", callback_data="toClearBinWarning")
            toBack = types.InlineKeyboardButton("To back", callback_data="backToProfile")
            trashMenu.add(toDeliver, toClearBin, toBack)



    else:
        if language == "RU":
            toBack = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
            trashMenu.add(toBack)

        if language == "EN":
            toBack = types.InlineKeyboardButton("To back", callback_data="backToProfile")
            trashMenu.add(toBack)

    return trashMenu


def areYouSureText(language):
    if language == "RU":
        return "Ты уверен?"

    if language == "EN":
        return "Are you sure?"


def areYouSureMenu(language):
    areYouSure = types.InlineKeyboardMarkup(row_width=1)

    if language == "RU":
        yes = types.InlineKeyboardButton("Очистить", callback_data="toClearBin")
        no = types.InlineKeyboardButton("Назад", callback_data="bin")
        return areYouSure.add(yes, no)

    if language == "EN":
        yes = types.InlineKeyboardButton("To empty", callback_data="toClearBin")
        no = types.InlineKeyboardButton("Back", callback_data="bin")
        return areYouSure.add(yes, no)


def beforeOrderText(address: str, comment: str, language: str):
    if address is not None:
        if language == "RU":
            return f'''Адрес: {address}
Комментарий к адресу: {comment if comment is not None else "не указан"}'''

        elif language == "EN":
            return f'''Address: {address}
Comment for address: {comment if comment is not None else "didn't point"}'''

    else:
        if language == "RU":
            return "Вы не указали адрес, укажите его для заказа"
        if language == "EN":
            return "You didn't point address. Point it for order"


def beforeOrderMenu(address: str, language: str, fullprice: int):
    confirmMenu = types.InlineKeyboardMarkup(row_width=1)

    if address is not None:

        if language == "RU":
            confirm = types.InlineKeyboardButton("Подтвердить", callback_data="toConfirm#{}".format(fullprice))
            badAddress = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
            return confirmMenu.add(confirm, badAddress)
        if language == "EN":
            confirm = types.InlineKeyboardButton("Confirm", callback_data="toConfirm#{}".format(fullprice))
            badAddress = types.InlineKeyboardButton("Back", callback_data="backToProfile")
            return confirmMenu.add(confirm, badAddress)

    else:
        badAddress = types.InlineKeyboardButton("Back", callback_data="backToProfile")
        return confirmMenu.add(badAddress)


def chooseMethodPayText(language: str):
    if language == "RU":
        return "Выбери способ оплаты"

    if language == "EN":
        return "Choose method of pay"


def chooseMethodPayMenu(fullsum: int, language: str):
    methodsPay = types.InlineKeyboardMarkup(row_width=1)

    if language == "RU":
        forCash = types.InlineKeyboardButton("Наличные", callback_data="forCash#{}".format(fullsum))
        forCard = types.InlineKeyboardButton("Криптовалюта", callback_data="forCryptocurrency#{}".format(fullsum))
        toBack = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
        return methodsPay.add(forCash, forCard, toBack)

    if language == "EN":
        forCash = types.InlineKeyboardButton("Cash payment", callback_data="forCash#{}".format(fullsum))
        forCard = types.InlineKeyboardButton("Сryptocurrency", callback_data="forCryptocurrency#{}".format(fullsum))
        toBack = types.InlineKeyboardButton("Back", callback_data="backToProfile")
        return methodsPay.add(forCash, forCard, toBack)


def infoOrderText(products: list, fullsum: int, address: str, comment: str, payment: str, language: str):
    if len(products) != 0:

        if language == "RU":

            head = "Товаров: {}\n\nТовары:\n".format(len(products))

            for product in products:

                if pm.getPrice(product.idFromProduct) != 0:

                    name = product.nameOfProduct

                    price = pm.getPrice(product.idFromProduct)
                    num = product.numOfProducts
                    summ = num * price

                    head += "{} - {} грамм - {} BATH\n".format(name, num, summ)

                else:
                    name = product.split('#')[0]
                    head += 'Товар "{}" удален из магазина\n'.format(name)

            head += "\nИтого: {} BATH".format(fullsum)
            head += "\n\n\nАдрес: {}" \
                    "\n\nКомментарий к адресу: {}\n\n".format(address, comment if comment is not None else "не указан")

            if payment == "forCash":
                head += "Метод оплаты: наличные"

            return head

        if language == "EN":

            head = "Items: {}\n\nItems:\n".format(len(products))

            for product in products:

                if pm.getPrice(product.idFromProduct) != 0:

                    name = product.nameOfProduct

                    price = pm.getPrice(product.idFromProduct)
                    num = product.numOfProducts
                    summ = num * price

                    head += "{} - {} gramm - {} BATH\n".format(name, num, summ)

                else:
                    name = product.split('#')[0]
                    head += 'Item "{}" was delete from shop\n'.format(name)

            head += "\nTotal: {} BATH".format(fullsum)
            head += "\n\n\nAddress: {}" \
                    "\n\nComment for address: {}\n\n".format(address,
                                                             comment if comment is not None else "didn't point")

            if payment == "forCash":
                head += "Payment: cash"

            return head

    else:
        if language == "RU":
            return "Твоя корзина пуста ;("
        if language == "EN":
            return "Your trash is empty ;("


def infoOrderMenu(fullprice: int, payment: str, language):
    orderMenu = types.InlineKeyboardMarkup(row_width=1)

    if language == "RU":
        orderConfirm = types.InlineKeyboardButton("Подтвердить",
                                                  callback_data="orderConfirm#{}#{}".format(fullprice, payment))
        orderRefuse = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
        return orderMenu.add(orderConfirm, orderRefuse)

    if language == "EN":
        orderConfirm = types.InlineKeyboardButton("Confirm",
                                                  callback_data="orderConfirm#{}#{}".format(fullprice, payment))
        orderRefuse = types.InlineKeyboardButton("Back", callback_data="backToProfile")
        return orderMenu.add(orderConfirm, orderRefuse)


def confirmedOrderText(numberOfOrder: int, language: str):
    if language == "RU":
        return f'''Номер заказа: №{numberOfOrder}
Заказ успешно создан
Мы оповестим тебя, курьер примет заказ'''

    if language == "EN":
        return f'''Number of order: №{numberOfOrder}
Order created succesfully
We'll say you, when courier accepted the order'''


def confirmedOrderMenu(numberOfOrder: int, language: str):
    confirmedOrderMenu = types.InlineKeyboardMarkup(row_width=1)

    if language == "RU":
        toCurrentOrder = types.InlineKeyboardButton("К заказу", callback_data="toCurrentOrder#{}".format(numberOfOrder))
        toBack = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
        return confirmedOrderMenu.add(toCurrentOrder, toBack)

    if language == "EN":
        toCurrentOrder = types.InlineKeyboardButton("To order", callback_data="toCurrentOrder#{}".format(numberOfOrder))
        toBack = types.InlineKeyboardButton("Back", callback_data="backToProfile")
        return confirmedOrderMenu.add(toCurrentOrder, toBack)


class sliderOrderPaginator(InlineKeyboardPaginator):
    first_page_label = ''
    previous_page_label = ' < '
    next_page_label = ' > '
    last_page_label = ''


def textOrder(active, refusal, complete, language):
    if len(active + refusal + complete) != 0:
        if language == "RU":
            return 'Все ваши заказы:\n\n🟡 - заказ в процессе\n🔴 - заказ отменён\n🟢 - заказ завершён'

        if language == "EN":
            return 'All your orders:\n\n🟡 - active order\n🔴 - refused order\n🟢 - completed order'
    else:
        if language == "RU":
            return 'У тебя еще нет заказов ;('

        if language == "EN":
            return "You haven't orders yet ;("


def sliderOrder(page, active, refusal, complete, language):
    # print("---", refusal)
    active.reverse()
    refusal.reverse()
    complete.reverse()
    # print("---", refusal)

    orders = active + refusal + complete

    if len(orders) != 0:
        a = len(active)
        r = len(refusal)
        total = len(orders)

        paginator = sliderOrderPaginator(
            page_count=total,
            current_page=page,
            data_pattern='order#{page}'
        )

        paginator.current_page_label = '· {} ·'
        print(orders[page - 1])
        if orders[page - 1] in active:
            lookOrder = types.InlineKeyboardButton("№{} | {} BATH 🟡".format(str(orders[page - 1]).split('-#-#-')[0],
                                                                            str(orders[page - 1]).split('-#-#-')[3]),
                                                   callback_data="lookActive#{}".format(page - 1))
            paginator.add_before(lookOrder)

        elif orders[page - 1] in refusal:
            lookOrder = types.InlineKeyboardButton("№{} | {} BATH 🔴".format(str(orders[page - 1]).split('-#-#-')[9],
                                                                            str(orders[page - 1]).split('-#-#-')[3]),
                                                   callback_data="lookRefusal#{}".format(page - 1 - a))
            paginator.add_before(lookOrder)

        elif orders[page - 1] in complete:

            lookOrder = types.InlineKeyboardButton("№{} | {} BATH 🟢".format(str(orders[page - 1]).split('-#-#-')[9],
                                                                            str(orders[page - 1]).split('-#-#-')[3]),
                                                   callback_data="lookComplete#{}".format(page - 1 - a - r))
            paginator.add_before(lookOrder)

        if language == "RU":

            toBackButton = types.InlineKeyboardButton('Назад', callback_data='backToProfile')
            paginator.add_after(toBackButton)

        elif language == "EN":

            toBackButton = types.InlineKeyboardButton('Back', callback_data='backToProfile')
            paginator.add_after(toBackButton)

        return paginator.markup

    else:
        backingMenu = types.InlineKeyboardMarkup(row_width=1)

        if language == "RU":
            backingButton = types.InlineKeyboardButton("Назад", callback_data="backToProfile")
            return backingMenu.add(backingButton)
        if language == "EN":
            backingButton = types.InlineKeyboardButton("Back", callback_data="backToProfile")
            return backingMenu.add(backingButton)


def showActiveOrderText(activeOrders: list, choosedOrder: int, language: str):
    print(activeOrders)
    activeOrders.reverse()
    order = activeOrders[choosedOrder]
    order = str(order)

    if language == "RU":
        head = f"Заказ №{order.split('-#-#-')[0]}\n\nТовары:\n"
        items = order.split('-#-#-')[2]

        for item in items[:-1].split(','):
            head += "{} - {} грамм - {} BATH\n".format(
                item.split('#')[0],
                item.split('#')[1],
                int(item.split('#')[1]) * int(item.split('#')[2])
            )

        head += f"\n\nИтого: {order.split('-#-#-')[3]} BATH"
        head += f"\n\nДата и время заказа: {order.split('-#-#-')[4]}"
        head += f"\n\nСпособ оплаты: {order.split('-#-#-')[5]}"
        head += f"\n\nАдрес для заказа: {order.split('-#-#-')[7]}"
        head += f"\n\nКомментарий к адресу: " \
                f"{order.split('-#-#-')[8] if order.split('-#-#-')[8] != 'None' else 'не указан'}"
        head += f"\n\nСтатус заказа: {order.split('-#-#-')[6]}"
        return head

    if language == "EN":
        head = f"Order №{order.split('-#-#-')[0]}\n\nItems:\n"
        items = order.split('-#-#-')[2]

        for item in items[:-1].split(','):
            head += "{} - {} gramm - {} BATH\n".format(
                item.split('#')[0],
                item.split('#')[1],
                int(item.split('#')[1]) * int(item.split('#')[2])
            )

        head += f"\n\nTotal: {order.split('-#-#-')[3]} BATH"
        head += f"\n\nDate and time order: {order.split('-#-#-')[4]}"
        head += f"\n\nPayment: {'cash' if order.split('-#-#-')[5] == 'наличные' else '-'}"
        head += f"\n\nAddress for order: {order.split('-#-#-')[7]}"
        head += f"\n\nComment for address: " \
                f"{order.split('-#-#-')[8] if order.split('-#-#-')[8] != 'None' else 'didnt point'}"
        head += f"\n\nStatus order: {'waiting for courier' if order.split('-#-#-')[6] == 'ожидает курьера' else 'sent for delivety'}"
        return head


def showActiveOrderMenu(activeOrders: list, choosedOrder: int, language: str):
    showActiveOrderMenu = types.InlineKeyboardMarkup(row_width=1)


    activeOrders.reverse()
    idActive = activeOrders[choosedOrder].id


    if language == "RU":
        # добавить id ордера в колбэк дату
        toWriteCourier = types.InlineKeyboardButton("Написать курьеру", callback_data=f"toWriteCourier#{idActive}")
        toBack = types.InlineKeyboardButton("Назад", callback_data='myOrders')
        return showActiveOrderMenu.add(toWriteCourier, toBack)

    if language == "EN":
        toWriteCourier = types.InlineKeyboardButton("To write courier", callback_data=f"toWriteCourier#{idActive}")
        toBack = types.InlineKeyboardButton("Back", callback_data='myOrders')
        return showActiveOrderMenu.add(toWriteCourier, toBack)


def showCompleteOrderText(completeOrders: list, choosedOrder: int, language: str):
    # print(completeOrders)
    completeOrders.reverse()
    order = completeOrders[choosedOrder]
    order = str(order)

    if language == "RU":
        head = f"Заказ №{order.split('-#-#-')[9]}\n\nТовары:\n"
        items = order.split('-#-#-')[2]

        for item in items[:-1].split(','):
            head += "{} - {} грамм - {} BATH\n".format(
                item.split('#')[0],
                item.split('#')[1],
                int(item.split('#')[1]) * int(item.split('#')[2])
            )

        head += f"\n\nИтого: {order.split('-#-#-')[3]} BATH"
        head += f"\n\nДата и время заказа: {order.split('-#-#-')[4]}"
        head += f"\n\nСпособ оплаты: {order.split('-#-#-')[5]}"
        head += f"\n\nАдрес для заказа: {order.split('-#-#-')[7]}"
        head += f"\n\nКомментарий к адресу: " \
                f"{order.split('-#-#-')[8] if order.split('-#-#-')[8] != 'None' else 'не указан'}"
        head += f"\n\nЗакрытие заказа: {order.split('-#-#-')[6]}"
        return head

    if language == "EN":
        head = f"Order №{order.split('-#-#-')[0]}\n\nItems:\n"
        items = order.split('-#-#-')[2]

        for item in items[:-1].split(','):
            head += "{} - {} gramm - {} BATH".format(
                item.split('#')[0],
                item.split('#')[1],
                int(item.split('#')[1]) * int(item.split('#')[2])
            )

        head += f"\n\nTotal: {order.split('-#-#-')[3]} BATH"
        head += f"\n\nDate and time order: {order.split('-#-#-')[4]}"
        head += f"\n\nPayment: {'cash' if order.split('-#-#-')[5] == 'наличные' else '-'}"
        head += f"\n\nAddress for order: {order.split('-#-#-')[7]}"
        head += f"\n\nComment for address: " \
                f"{order.split('-#-#-')[8] if order.split('-#-#-')[8] != 'None' else 'didnt point'}"
        head += f"\n\nOrder closing: {order.split('-#-#-')[6]}"
        return head


def showCompleteOrderMenu(language: str):
    showCompleteOrderMenu = types.InlineKeyboardMarkup(row_width=1)

    if language == "RU":
        # добавить id ордера в колбэк дату
        toBack = types.InlineKeyboardButton("Назад", callback_data='myOrders')
        return showCompleteOrderMenu.add(toBack)

    if language == "EN":
        toBack = types.InlineKeyboardButton("Back", callback_data='myOrders')
        return showCompleteOrderMenu.add(toBack)


def showRefusalOrderText(refusalOrders: list, choosedOrder: int, language: str):
    # print(refusalOrders)
    refusalOrders.reverse()
    order = refusalOrders[choosedOrder]
    order = str(order)

    if language == "RU":
        head = f"Заказ №{order.split('-#-#-')[9]}\n\nТовары:\n"
        items = order.split('-#-#-')[2]

        for item in items[:-1].split(','):
            head += "{} - {} грамм - {} BATH\n".format(
                item.split('#')[0],
                item.split('#')[1],
                int(item.split('#')[1]) * int(item.split('#')[2])
            )

        head += f"\n\nИтого: {order.split('-#-#-')[3]} BATH"
        head += f"\n\nДата и время заказа: {order.split('-#-#-')[4]}"
        head += f"\n\nСпособ оплаты: {order.split('-#-#-')[5]}"
        head += f"\n\nАдрес для заказа: {order.split('-#-#-')[7]}"
        head += f"\n\nКомментарий к адресу: " \
                f"{order.split('-#-#-')[8] if order.split('-#-#-')[8] != 'None' else 'не указан'}"
        head += f"\n\nЗакрытие заказа: {order.split('-#-#-')[6]}"
        head += f"\nПричина закрытия: {order.split('-#-#-')[10]}"
        return head

    if language == "EN":
        head = f"Order №{order.split('-#-#-')[0]}\n\nItems:\n"
        items = order.split('-#-#-')[2]

        for item in items[:-1].split(','):
            head += "{} - {} gramm - {} BATH".format(
                item.split('#')[0],
                item.split('#')[1],
                int(item.split('#')[1]) * int(item.split('#')[2])
            )

        head += f"\n\nTotal: {order.split('-#-#-')[3]} BATH"
        head += f"\n\nDate and time order: {order.split('-#-#-')[4]}"
        head += f"\n\nPayment: {'cash' if order.split('-#-#-')[5] == 'наличные' else '-'}"
        head += f"\n\nAddress for order: {order.split('-#-#-')[7]}"
        head += f"\n\nComment for address: " \
                f"{order.split('-#-#-')[8] if order.split('-#-#-')[8] != 'None' else 'didnt point'}"
        head += f"\n\nOrder closing: {order.split('-#-#-')[6]}"
        head += f"\nReason of refusal: {order.split('-#-#-')[10]}"
        return head


class sliderChangeBinPaginator(InlineKeyboardPaginator):
    first_page_label = ''
    previous_page_label = ' - '
    next_page_label = ' + '
    last_page_label = ''


def textBinProduct(language):
    if language == "RU":
        return 'Изменение.......'

    elif language == "EN":
        return 'Changing.......'


def sliderChangeBin(page, product, language):
    paginator = sliderChangeBinPaginator(
        page_count=500,
        current_page=page,
        data_pattern='binslide#' + str(product.id) + '#{page}'
    )
    paginator.current_page_label = '· {} ·'

    if language == "RU":

        productInfo = types.InlineKeyboardButton(f"{product.nameOfProduct} | "
                                                 f"{pm.getPrice(product.idFromProduct) * product.numOfProducts} BATH",
                                                 callback_data='nowork')

        toDeleteButton = types.InlineKeyboardButton('Удалить', callback_data=f'DeleteFromBin#{product.id}')
        toBackButton = types.InlineKeyboardButton('Назад', callback_data='bin')
        paginator.add_before(productInfo)
        paginator.add_after(toBackButton, toDeleteButton)

    elif language == "EN":

        productInfo = types.InlineKeyboardButton(f"{product.nameOfProduct} | "
                                                 f"{pm.getPrice(product.idFromProduct) * product.numOfProducts} BATH",
                                                 callback_data='nowork')

        toDeleteButton = types.InlineKeyboardButton('Delete', callback_data=f'DeleteFromBin#{product.id}')
        toBackButton = types.InlineKeyboardButton('Back', callback_data='bin')
        paginator.add_before(productInfo)
        paginator.add_after(toBackButton, toDeleteButton)

    return paginator.markup


def deletedItemText(name, language):
    if language == "RU":
        return f'Ты совершил ошибку, удалив "{name}"'
    if language == "EN":
        return f'You made a mistake: "{name}" deleted'


toAdminText = "Администрирование"
password = "123"

def toEnterPasswordText():
    return "Введите пароль доступа"

def passwordCorrectText():
    return "Доступ одобрен"

def passwordUncorrectText():
    return "Отказано в доступе"

def helloBoss():
    return "Привет, Босс!"

def helloMenu():
    bossMenu = types.InlineKeyboardMarkup(row_width=1)

    orders = types.InlineKeyboardButton("Заказы", callback_data="adminOrders")
    postSale = types.InlineKeyboardButton("Пост-акция", callback_data="adminPostSale")
    catalog = types.InlineKeyboardButton("Каталог товаров", callback_data="adminCatalog")

    return bossMenu.add(orders, postSale, catalog)

def mainAdmin():
    adminMainMenu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    adminMainButton = types.KeyboardButton("На главную")
    return adminMainMenu.add(adminMainButton)


chooseListOrdersText = "Выбери список заказов"

def chooseListOrdersMenu():
    chooseListOrdersMenu = types.InlineKeyboardMarkup(row_width=1)
    listActive = types.InlineKeyboardButton("Активные", callback_data="activeList")
    listRefusal = types.InlineKeyboardButton("Отмененные", callback_data="refusalList")
    listComplete = types.InlineKeyboardButton("Завершенные", callback_data="completeList")
    toBack = types.InlineKeyboardButton("Назад", callback_data="toMainAdmin")
    return chooseListOrdersMenu.add(listActive, listRefusal, listComplete, toBack)


class adminSliderOrderPaginator(InlineKeyboardPaginator):
    first_page_label = '<<'
    previous_page_label = ' < '
    next_page_label = ' > '
    last_page_label = '>>'


def AdminTextOrderActive(active):
    if len(active) != 0:
        return 'Список активных заказов:'
    else:
        return 'Активных заказов нет ;('


def adminSliderOrderActive(page, active):


    if len(active) != 0:

        paginator = adminSliderOrderPaginator(
            page_count=len(active),
            current_page=page,
            data_pattern='adminActiveOrder#{page}'
        )

        paginator.current_page_label = '· {} ·'

        adminLookActive = types.InlineKeyboardButton("№{} | {} BATH 🟡".format(str(active[page - 1].id),
                                                                              str(active[page - 1].fullprice)),
                                                     callback_data="adminLookActive#{}".format(page - 1))
        paginator.add_before(adminLookActive)

        toBackButton = types.InlineKeyboardButton('Назад', callback_data='adminOrders')
        paginator.add_after(toBackButton)

        return paginator.markup

    else:
        backingMenu = types.InlineKeyboardMarkup(row_width=1)

        backingButton = types.InlineKeyboardButton("Назад", callback_data="adminOrders")
        return backingMenu.add(backingButton)



def adminActiveInfoText(activeOrders: list, choosedOrder: int):

    order = activeOrders[choosedOrder]
    customer = db.getCustomer(order.customer_id)
    head = f"Заказ №{order.id}\n\n"
    if db.getCustomer(order.customer_id).username is not None:
        head += f'Покупатель: @{customer.username}\n\n'
    head += f'Язык: {customer.language}\n\n'
    head += 'Товары:\n'
    items = order.items

    for item in items[:-1].split(','):
        head += "{} - {} грамм - {} BATH\n".format(
            item.split('#')[0],
            item.split('#')[1],
            int(item.split('#')[1]) * int(item.split('#')[2])
        )

    head += f"\n\nИтого: {order.fullprice} BATH"
    head += f"\n\nДата и время заказа: {order.datetime}"
    head += f"\n\nСпособ оплаты: {order.methodpay}"
    head += f"\n\nАдрес для заказа: {order.address}"
    head += f"\n\nКомментарий к адресу: " \
            f"{order.comment if order.comment is not None else 'не указан'}"
    head += f"\n\nСтатус заказа: {order.status}"
    return head

def adminActiveInfoMenu(activeOrders: list, choosedOrder: int):
    order = activeOrders[choosedOrder]
    activeMenu = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Написать покупателю",
                                         callback_data=f"messageToCustomer#{order.customer_id}#{order.id}#{choosedOrder}")

    button3 = types.InlineKeyboardButton("Отменить заказ",
                                         callback_data=f"refusingActive#{order.id}#{choosedOrder}")

    button4 = types.InlineKeyboardButton("Завершить заказ",
                                         callback_data=f"completingActive#{order.id}")

    button5 = types.InlineKeyboardButton("Назад", callback_data="activeList")

    activeMenu.add(button1)

    if order.status == "ожидает курьера":
        activeMenu.add(types.InlineKeyboardButton("Обновить статус-принять к доставке",
                                         callback_data=f"acceptingActive#{order.id}#{choosedOrder}"))

    activeMenu.add(button3, button4, button5)

    return activeMenu

def switchStatusText():
    return "Статус заказа успешно обновлен\nПокупатель получил уведомление"

def switchActiveToCompleteText(id: int):
    return f"Заказ №{id} успешно завершен"

def switchActiveToCompleteMenu():
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Назад", callback_data="activeList"))

def switchActiveToRefusalText(language):
    return f"Введите причину отмены или вернитесь назад!\nРекомендуется использовать язык: {language}"
def switchActiveToRefusalMenu(page: int):
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Назад", callback_data=f"activeToRefusalCancel#{page}"))

def infoActiveToRefusalText(id: int):
    return f"Заказ №{id} успешно отменён\nПокупатель получил уведомление"

def infoActiveToRefusalMenu():
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Назад", callback_data="activeList"))

def toCommunicateWithCustomerText(id: int):
    return f"Напишите сообщение для покупателя\nпо заказу №{id}\n" \
           f"Рекомендуется использовать язык: {db.getLanguage(ao.getActiveOrder(id).customer_id)}"

def toCommunicateWithCustomerMenu(page: int):
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Назад",
                                                                       callback_data=f"adminCommunicateCancel#{page}"))

def answerNextSendToCustomerText(idOrder: int):
    return f'Сообщение покупателю по заказу №{idOrder} успешно отправлено'

def answerNextSendToCustomerMenu(page: int):
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Назад", callback_data=f"adminLookActive#{page}"))

def sendingToCustomerText(idOrder, text, language):
    if language == "RU":
        return f"Вам сообщение от продавца по заказу №{idOrder}:\n" + text
    if language == "EN":
        return f'You get message from seller on order №{idOrder}:\n' + text
def sendingToCustomerMenu(idOrder, idAdmin, language):
    if language == "RU":
        return types.InlineKeyboardMarkup().\
            add(types.InlineKeyboardButton("Ответить", callback_data=f"toAnswerToAdmin#{idAdmin}#{idOrder}"))
    if language == "EN":
        return types.InlineKeyboardMarkup(). \
            add(types.InlineKeyboardButton("To answer", callback_data=f"toAnswerToAdmin#{idAdmin}#{idOrder}"))

def toAnswerToAdminText(language):
    if language == "RU":
        return 'Напиши сообщение:'
    if language == "EN":
        return 'Write a message:'
def toAnswerToAdminMenu(language):
    if language == "RU":
        return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Отменить", callback_data="answerToAdminCancel"))
    if language == "EN":
        return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Cancel", callback_data="answerToAdminCancel"))
def feedbackToCustomerAfterSendAdminText(language):
    if language == "RU":
        return "Сообщение успешно отправлено"
    if language == "EN":
        return "Message has sent successfully"

def sendingToAdminText(idOrder, text):
    return f'Поступило сообщение от пользователя по заказу №{idOrder}:\n' + text

def sendingToAdminMenu(idOrder, idCustomer):
    return types.InlineKeyboardMarkup().\
        add(types.InlineKeyboardButton("Ответить", callback_data=f"messageToCustomer#{idCustomer}#{idOrder}"))

def toAnswerToCustomerMenu(page: int):
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Посмотреть его заказ",
                                                                       callback_data=f"adminCommunicateCancel#{page}"))

def AdminTextOrderRefusal(active):
    if len(active) != 0:
        return 'Список отменённых заказов:'
    else:
        return 'Отменённых заказов нет ;('
def adminSliderOrderRefusal(page, refusal):

    if len(refusal) != 0:

        paginator = adminSliderOrderPaginator(
            page_count=len(refusal),
            current_page=page,
            data_pattern='adminRefusalOrder#{page}'
        )

        paginator.current_page_label = '· {} ·'

        adminLookActive = types.InlineKeyboardButton("№{} | {} BATH 🔴".format(str(refusal[page - 1].id_from_active),
                                                                              str(refusal[page - 1].fullprice)),
                                                     callback_data="adminLookRefusal#{}".format(page - 1))
        paginator.add_before(adminLookActive)

        toBackButton = types.InlineKeyboardButton('Назад', callback_data='adminOrders')
        paginator.add_after(toBackButton)

        return paginator.markup

    else:
        backingMenu = types.InlineKeyboardMarkup(row_width=1)

        backingButton = types.InlineKeyboardButton("Назад", callback_data="adminOrders")
        return backingMenu.add(backingButton)

def adminRefusalInfoText(refusalOrders: list, choosedOrder: int):

    order = refusalOrders[choosedOrder]

    customer = db.getCustomer(order.customer_id)
    head = f"Заказ №{order.id}\n\n"
    if db.getCustomer(order.customer_id).username is not None:
        head += f'Покупатель: @{customer.username}\n\n'
    head += f'Язык: {customer.language}\n\n'
    head += 'Товары:\n'

    items = order.items

    for item in items[:-1].split(','):
        head += "{} - {} грамм - {} BATH\n".format(
            item.split('#')[0],
            item.split('#')[1],
            int(item.split('#')[1]) * int(item.split('#')[2])
        )

    head += f"\n\nИтого: {order.fullprice} BATH"
    head += f"\n\nДата и время заказа: {order.datetime}"
    head += f"\n\nДата и время отказа: {order.datetime_refuse}"
    head += f"\n\nСпособ оплаты: {order.methodpay}"
    head += f"\n\nАдрес для заказа: {order.address}"
    head += f"\n\nКомментарий к адресу: " \
            f"{order.comment if order.comment is not None else 'не указан'}"
    head += f"\n\nПричина отказа: {order.reason}"
    return head

def adminRefusalInfoMenu():

    return types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("Назад", callback_data="refusalList"))

def AdminTextOrderComplete(complete: list):
    if len(complete) != 0:
        return 'Список завершенных заказов:'
    else:
        return 'Завершенных заказов нет!'
def adminSliderOrderComplete(page, complete):

    if len(complete) != 0:

        paginator = adminSliderOrderPaginator(
            page_count=len(complete),
            current_page=page,
            data_pattern='adminCompleteOrder#{page}'
        )

        paginator.current_page_label = '· {} ·'

        adminLookActive = types.InlineKeyboardButton("№{} | {} BATH 🟢".format(str(complete[page - 1].id_from_active),
                                                                              str(complete[page - 1].fullprice)),
                                                     callback_data="adminLookComplete#{}".format(page - 1))
        paginator.add_before(adminLookActive)

        toBackButton = types.InlineKeyboardButton('Назад', callback_data='adminOrders')
        paginator.add_after(toBackButton)

        return paginator.markup

    else:
        backingMenu = types.InlineKeyboardMarkup(row_width=1)

        backingButton = types.InlineKeyboardButton("Назад", callback_data="adminOrders")
        return backingMenu.add(backingButton)

def adminCompleteInfoText(completeOrders: list, choosedOrder: int):

    order = completeOrders[choosedOrder]

    customer = db.getCustomer(order.customer_id)
    head = f"Заказ №{order.id}\n\n"
    if db.getCustomer(order.customer_id).username is not None:
        head += f'Покупатель: @{customer.username}\n\n'
    head += f'Язык: {customer.language}\n\n'
    head += 'Товары:\n'

    items = order.items

    for item in items[:-1].split(','):
        head += "{} - {} грамм - {} BATH\n".format(
            item.split('#')[0],
            item.split('#')[1],
            int(item.split('#')[1]) * int(item.split('#')[2])
        )

    head += f"\n\nИтого: {order.fullprice} BATH"
    head += f"\n\nДата и время заказа: {order.datetime}"
    head += f"\n\nДата и время завершения: {order.datetime_complete}"
    head += f"\n\nСпособ оплаты: {order.methodpay}"
    head += f"\n\nАдрес для заказа: {order.address}"
    head += f"\n\nКомментарий к адресу: " \
            f"{order.comment if order.comment is not None else 'не указан'}"
    return head

def adminCompleteInfoMenu():

    return types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("Назад", callback_data="completeList"))

def showNewActiveOrderText(idOrder):
    return f'Поступил новый заказ №{idOrder}'
def showNewActiveOrderMenu(page: int):
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Посмотреть заказ",
                                                                       callback_data=f"adminCommunicateCancel#{page}"))

def infoReason(idOrder, text, language):
    if language == "RU":
        return f"Продавец отменил заказ №{idOrder}\nПричина: {text}"
    elif language == "EN":
        return f'Seller has refused order №{idOrder}\nReason: {text}'
def infoAccept(idOrder, language):
    if language == "RU":
        return f'Заказ №{idOrder} принят в доставку'

    elif language == "EN":
        return f'Order №{idOrder} was sent for delivery'

def adminBeforePostTextRU():
    return "Введите текст поста на русском языке:"

def adminBeforePostTextEN():
    return "Введите текст поста на английском языке:"
def adminBeforePostMenu():
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Сбросить", callback_data="resetPost"))
def adminGetTypePostText(textRU, textEN):
    return f"Текст для русских пользователей:\n{textRU}\n\nТекст на англоязычных пользователей:\n{textEN}\n\nВыберите вложение для поста"
def adminGetTypePostMenu():
    menu = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("Видео", callback_data=f"attachVideo")
    b2 = types.InlineKeyboardButton("Фото", callback_data=f"attachPhoto")
    b3 = types.InlineKeyboardButton("Без вложения", callback_data=f"noAttach")
    b4 = types.InlineKeyboardButton("Сбросить", callback_data="resetPost")
    return menu.add(b1, b2, b3, b4)


def adminPostToAttachPhoto():
    return 'Прикрепите и отправьте фото:'

def adminPostToAttachVideo():
    return f'Прикрепите видео в формате mp4:'

def adminFinalPostText(textRU, textEN):
    return f"Текст для русских пользователей:\n{textRU}\n\nТекст на англоязычных пользователей:\n{textEN}"

def adminFinalPostMenu():
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Опубликовать", callback_data="adminToPublishPost"),
        types.InlineKeyboardButton("Сбросить", callback_data="resetPost")
    )

def adminListProductText(products):
    if len(products) != 0:
        return 'Выберите товар для просмотра или удаления'
    else:
        return 'Сейчас товаров нет в магазине'

def adminSliderShop(page, products):
    if len(products) != 0:

        nameOfProducts = list(i.name for i in products)
        idOrders = list(i.id for i in products)
        paginator = sliderShopPaginator(page_count=len(products),
                                        current_page=page,
                                        data_pattern='adminListProduct#{page}')

        lookProduct = types.InlineKeyboardButton('{}'.format(nameOfProducts[page - 1]),
                                                 callback_data='adminProductName#{}'.format(idOrders[page - 1]))
        paginator.add_before(lookProduct)

        toAddProduct = types.InlineKeyboardButton('Добавить товар', callback_data='adminAddProduct')

        toBackButton = types.InlineKeyboardButton('Назад', callback_data='toMainAdmin')
        paginator.add_after(toBackButton, toAddProduct)

        return paginator.markup

    else:
        return types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('Добавить товар', callback_data='adminAddProduct'),
            types.InlineKeyboardButton("Назад", callback_data="toMainAdmin")
        )



def adminTextProduct(product):
    return f'''ВЗГЛЯДОМ RU ПОЛЬЗОВАТЕЛЯ:\n
{product.name}
{product.infoAbout}

Доставка по всему острову
1 грамм - {product.price} BATH


ВЗГЛЯДОМ EN ПОЛЬЗОВАТЕЛЯ:\n
{product.name}
{product.infoAbout}

Delivery on the whole Island
1 gram - {product.price} BATH'''

def adminProductMenu(idOrder):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Изменить название", callback_data=f"adminChangeName#{idOrder}"),
        types.InlineKeyboardButton("Изменить описание", callback_data=f"adminChangeInfoAbout#{idOrder}"),
        types.InlineKeyboardButton("Изменить цену", callback_data=f"adminChangePrice#{idOrder}"),
        types.InlineKeyboardButton("Удалить товар", callback_data=f"adminDeleteProduct#{idOrder}"),
        types.InlineKeyboardButton("Назад", callback_data="adminCatalogFromMedia")
    )

def delProductText():
    return "Товар удален из магазина"

def adminAddProductName():
    return 'Введите название товара\n(Кратко, чтобы вместилось в кнопку)'

def adminAddProductNameMenu():
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Сбросить", callback_data="resetProduct"))

def adminAddProductText():
    return 'Введите описание товара:'

def adminAddProductPrice():
    return 'Введите цену за 1 грамм в валюте BATH:'

def adminAddProductMediaText(product):
    return f'''ВЗГЛЯДОМ RU ПОЛЬЗОВАТЕЛЯ:\n
{product.name}
{product.infoAbout}

Доставка по всему острову
1 грамм - {product.price} BATH


ВЗГЛЯДОМ EN ПОЛЬЗОВАТЕЛЯ:\n
{product.name}
{product.infoAbout}

Delivery on the whole Island
1 gram - {product.price} BATH


Выберите тип вложения:'''

def adminAddProductMediaMenu():
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Видео", callback_data=f"attachVideoToProduct"),
        types.InlineKeyboardButton("Фото", callback_data=f"attachPhotoToProduct"),
        types.InlineKeyboardButton("Сбросить", callback_data="resetProduct")
    )
def adminFinalProductMenu():
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton("Добавить в начало", callback_data="addProductInStart"),
        types.InlineKeyboardButton("Добавить в конец", callback_data="addProductInFinish"),
        types.InlineKeyboardButton("Сбросить", callback_data="resetProduct")
    )

def feedbackAdminNewPost():
    return "Товар добавлен в магазин\nПользователи получили уведомления"

def feedbackNewPost(language):
    if language == "RU":
        return "Загляни в магазин!\nТам кое что новенькое и интересное"
    elif language == "EN":
        return "Look to shop\nThere is something new and interesting"


def adminChangeMenu(idProduct):
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Назад", callback_data=f"resetChanging#{idProduct}"))