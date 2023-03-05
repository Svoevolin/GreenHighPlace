from app.config import db, app
from .CustomerModel import Customer
from app.models import CartModel as cart
from datetime import datetime
from app.models import ProductModel as pm
from app.models import ActiveOrderModel as ao

# from CustomerModel import Customer
# import os,sys
# sys.path.insert(1, os.path.join(sys.path[0], '../'))
# from config import app, db


class CompleteOrder(db.Model):
    __tablename__ = 'complete'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    items = db.Column(db.String, nullable=False)
    fullprice = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.String(64), nullable=False)
    methodpay = db.Column(db.String(64), nullable=True)
    datetime_complete = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=True)
    id_from_active = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"{self.id}-#-#-{self.customer_id}-#-#-{self.items}" \
               f"-#-#-{self.fullprice}-#-#-{self.datetime}-#-#-{self.methodpay}-#-#-{self.datetime_complete}" \
               f"-#-#-{self.address}-#-#-{self.comment}-#-#-{self.id_from_active}"


def getAllCompleteOrders():
    try:
        with app.app_context():

            return CompleteOrder.query.filter(CompleteOrder.id is not None).all()

    except Exception as e:
        return print(e, "\ngetAllActiveOrders error")
def getCompleteOrder(customer_id: int):
    try:
        with app.app_context():

            return CompleteOrder.query.filter_by(customer_id=customer_id).all()

    except Exception as e:
        return print(e, "\ngetCompleteOrder error")

def getCompleteOrders(customer_id: int):
    try:
        with app.app_context():

            return CompleteOrder.query.filter_by(customer_id=customer_id).all()

    except Exception as e:
        return print(e, "\ngetCompleteOrders error")

def switcherActiveToComplete(active: ao.ActiveOrder):
    try:
        with app.app_context():
            complete = CompleteOrder(
                customer_id=active.customer_id,
                items=active.items,
                fullprice=active.fullprice,
                datetime=active.datetime,
                methodpay=active.methodpay,
                datetime_complete=str(datetime.now().strftime("%d/%m/%Y %H:%M")),
                address=active.address,
                comment=active.comment,
                id_from_active=active.id
            )

            db.session.delete(active)
            db.session.add(complete)
            db.session.commit()
            return 1

    except Exception as e:
        return print(e, "\nswitcherActiveToComplete error")

# def addActiveOrder(customer_id: int, fullprice: int, methodpay: str):
#     try:
#         with app.app_context():
#             products = cart.getCart(customer_id=customer_id)
#             items = ""
#             for product in products:
#                 product = str(product)
#                 name = product.split('#')[0]
#                 items += product + "#" + str(pm.getPrice(name)) + ","
#
#             dayandtime = str(datetime.now().strftime("%d/%m/%Y %H:%M"))
#             if methodpay == "forCash":
#
#                 order = ActiveOrder(customer_id=customer_id,
#                                     items=items,
#                                     fullprice=fullprice,
#                                     datetime=dayandtime,
#                                     methodpay="наличные")
#
#                 # numberOfOrder = order.id
#                 cart.delProductsFromCart(customer_id)
#
#                 db.session.add(order)
#
#                 db.session.commit()
#                 c = ActiveOrder.query.filter(ActiveOrder.id is not None).all()
#
#                 return c[-1].id
#     except Exception as e:
#         return print(e, "\naddActiveOrder error")


