from app.config import db, app
from .CustomerModel import Customer

# from CustomerModel import Customer
# import os,sys
# sys.path.insert(1, os.path.join(sys.path[0], '../'))
# from config import app, db


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.BigInteger, nullable=False)
    nameOfProduct = db.Column(db.String, nullable=False)
    numOfProducts = db.Column(db.Integer, nullable=False)
    idFromProduct = db.Column(db.Integer, nullable=False)

    # customer_id = db.Column(db.Integer, nullable=False)

    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # customer = db.relationship('Customer', backref=db.backref('cart', lazy=True))
    #
    # def __init__(self, customer: Customer, nameOfProduct: str, numOfProducts: int):

    #     with app.app_context():
    #         self.customer = customer
    #         self.nameOfProduct = nameOfProduct,
    #         self.numOfProducts = numOfProducts
    #
    #         customer.cart.append(self)
    #         current_db_sessions = db.object_session(customer)
    #         current_db_sessions.add(customer)
    #         current_db_sessions.commit()

    def __repr__(self):
        return f"{self.nameOfProduct}#{self.numOfProducts}"

def addToCart(customer_id: int, nameOfProduct: str, numOfProducts: int, idFromProduct = int):
    try:
        with app.app_context():
            cart = Cart(customer_id=customer_id, nameOfProduct=nameOfProduct,
                        numOfProducts=numOfProducts, idFromProduct=idFromProduct)
            db.session.add(cart)
            db.session.commit()

            return 1
    except Exception as e:
        return print(e, "\naddCustomer error")

def getCart(customer_id: int):
    try:
        with app.app_context():

            return Cart.query.filter_by(customer_id=customer_id).all()

    except Exception as e:
        return print(e, "\ngetOfNumberOfProducts error")

def getProductFromCart(id: int):
    try:
        with app.app_context():

            return Cart.query.filter_by(id=id).first()

    except Exception as e:
        return print(e, "\ngetProductFromCart error")

def changeNumOfProducts(id: int, numOfProducts: int):
    try:
        with app.app_context():
            product = Cart.query.filter_by(id=id).first()
            product.numOfProducts = numOfProducts
            db.session.commit()
    except Exception as e:
        return print(e, "\ngetProductFromCart error")
def getOfNumberOfProducts(customer_id: int):
    try:
        with app.app_context():

            return len(Cart.query.filter_by(customer_id=customer_id).all())

    except Exception as e:
        return print(e, "\ngetOfNumberOfProducts error")

def delProductFromCart(id: int):
    try:
        with app.app_context():
            product = Cart.query.filter_by(id=id).first()
            db.session.delete(product)
            db.session.commit()
    except Exception as e:
        return print(e, "\ngetOfNumberOfProducts error")
def delProductsFromCart(customer_id: int):
    try:
        with app.app_context():
            products = Cart.query.filter_by(customer_id=customer_id).all()
            for product in products:
                db.session.delete(product)
            db.session.commit()
    except Exception as e:
        return print(e, "\ngetOfNumberOfProducts error")

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