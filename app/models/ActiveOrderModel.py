from app.config import db, app
from .CustomerModel import Customer
from app.models import CartModel as cart
from datetime import datetime
from app.models import ProductModel as pm


# from CustomerModel import Customer
# import os,sys
# sys.path.insert(1, os.path.join(sys.path[0], '../'))
# from config import app, db


class ActiveOrder(db.Model):
    __tablename__ = 'active'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    items = db.Column(db.String, nullable=False)
    fullprice = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.String(64), nullable=False)
    methodpay = db.Column(db.String(64), nullable=True)
    status = db.Column(db.String(64), default="ожидает курьера")
    address = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"{self.id}-#-#-{self.customer_id}-#-#-{self.items}-#-#-{self.fullprice}-#-#-{self.datetime}" \
               f"-#-#-{self.methodpay}-#-#-{self.status}-#-#-{self.address}-#-#-{self.comment}"

def addActiveOrder(customer_id: int, fullprice: int, methodpay: str, address: str, comment: str):
    try:
        with app.app_context():
            products = cart.getCart(customer_id=customer_id)
            items = ""
            for product in products:
                # product = str(product)
                # name = product.split('#')[0]
                items += product.nameOfProduct + "#" + str(product.numOfProducts) + \
                         "#" + str(pm.getPrice(product.idFromProduct)) + ","

            dayandtime = str(datetime.now().strftime("%d/%m/%Y %H:%M"))
            if methodpay == "forCash":

                order = ActiveOrder(customer_id=customer_id,
                                    items=items,
                                    fullprice=fullprice,
                                    datetime=dayandtime,
                                    methodpay="наличные",
                                    address=address,
                                    comment=comment)

                # numberOfOrder = order.id
                cart.delProductsFromCart(customer_id)

                db.session.add(order)

                db.session.commit()
                c = ActiveOrder.query.filter(ActiveOrder.id is not None).all()

                return c[-1].id
    except Exception as e:
        return print(e, "\naddActiveOrder error")

def getActiveOrders(customer_id: int):
    try:
        with app.app_context():

            return ActiveOrder.query.filter_by(customer_id=customer_id).all()

    except Exception as e:
        return print(e, "\ngetActiveOrders error")

def switchStatus(id: int):
    try:
        with app.app_context():
            active = ActiveOrder.query.filter_by(id=id).first()
            active.status = "Передано на доставку"
            db.session.add(active)
            db.session.commit()
            return 1

    except Exception as e:
        return print(e, "\ngetActiveOrders error")

def getAllActiveOrders():
    try:
        with app.app_context():

            return ActiveOrder.query.filter(ActiveOrder.id is not None).all()

    except Exception as e:
        return print(e, "\ngetAllActiveOrders error")
def getActiveOrder(id: int):
    try:
        with app.app_context():

            return ActiveOrder.query.filter_by(id=id).first()

    except Exception as e:
        return print(e, "\ngetActiveOrders error")
def delFromActive(id: int):
    try:
        with app.app_context():
            active = ActiveOrder.query.filter_by(id=id).first()
            db.session.delete(active)
            db.session.commit()
    except Exception as e:
        return print(e, "\ngetOfNumberOfProducts error")




# def getCart(customer_id: int):
#     try:
#         with app.app_context():
#
#             return Cart.query.filter_by(customer_id=customer_id).all()
#
#     except Exception as e:
#         return print(e, "\ngetOfNumberOfProducts error")
#
# def getOfNumberOfProducts(customer_id: int):
#     try:
#         with app.app_context():
#
#             return len(Cart.query.filter_by(customer_id=customer_id).all())
#
#     except Exception as e:
#         return print(e, "\ngetOfNumberOfProducts error")
#
# def delProductsFromCart(customer_id: int):
#     try:
#         with app.app_context():
#             products = Cart.query.filter_by(customer_id=customer_id).all()
#             for product in products:
#                 db.session.delete(product)
#             db.session.commit()
#     except Exception as e:
#         return print(e, "\ngetOfNumberOfProducts error")

# def getCustomers():
#     try:
#         with app.app_context():
#             return Customer.query.filter(Customer.id != None).all()
#
#     except Exception as e:
#         return print(e, "\ngetCustomers error")

# def addToCart(customer: Customer, nameOfProduct: str, numOfProducts: int):
#     try:
#         with app.app_context():
#
#             print(customer)
#             c = Cart(customer=customer,
#                      nameOfProduct=nameOfProduct,
#                      numOfProducts=numOfProducts)
#             print(c)
#             customer.cart.append(c)
#             current_db_sessions = db.object_session(customer)
#             current_db_sessions.add(customer)
#             current_db_sessions.commit()
#
#             return 1
#     except Exception as e:
#         return print(e, "\naddToCart error")
#
# def getOfNumberOfProducts(customer: Customer):
#     try:
#         with app.app_context():
#             return len(customer.cart)
#     except Exception as e:
#         return print(e, "\naddToCart error")