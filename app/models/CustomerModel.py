from app.config import db, app
from app.logger import Logger
from app.utils import databaseResponseModel
from typing import Optional

log = Logger()

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    chatId = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), default="N/A")
    dateLogin = db.Column(db.String(64), default="N/A")
    refCode = db.Column(db.String(64), default="N/A")

    # api_hash = db.Column(db.String(128), nullable=False)
    # phone = db.Column(db.String(32), nullable=False)
    # username = db.Column(db.String(128), nullable=False)
    # host = db.Column(db.String(32), nullable=True)
    # port = db.Column(db.String(32), nullable=True)
    # public_key = db.Column(db.String(512), nullable=True)

    def __repr__(self):
        return '<Account %r>' % self.username

def addCustomer(chatId: int, username: str, dateLogin: str, refCode: str):
    try:
        with app.app_context():
            if Customer.query.filter_by(chatId=chatId).first():
                return {"message": 'User already added'}
            else:
                customer = Customer(chatId=chatId, username=username, dateLogin=dateLogin,
                                    refCode=refCode, language='N/A')
                db.session.add(customer)
                db.session.commit()

            return {"message": 'Customer added', "name": customer.chatId}
    except Exception as e:
        return print(e, "\naddCustomer error")


def setLanguage(chatId, language):
    try:
        with app.app_context():
            if Customer.query.filter_by(chat_id=chatId).first():
                customer = Customer.query.filter_by(chat_id=chatId).first()
                customer.language = language
                db.session.commit()
                return {"message": f'Language set is{customer.language}', "status": True}
            else:
                return {"message": 'No user with this chatId', "status": False}

    except Exception as e:
        return print(e, "\nsetLanguage error")

def getLanguage(chatId):
    try:
        with app.app_context():
            if Customer.query.filter_by(chatId=chatId).first():
                customer = Customer.query.filter_by(chatId=chatId).first()
                return customer.language
            else:
                return {"message": 'No user with this chatId', "status": False}

    except Exception as e:
        return print(e, "\ngetLanguage error")

def getCustomers():
    try:
        with app.app_context():
            return Customer.query.filter(Customer.id != None).all()

    except Exception as e:
        return print(e, "\ngetCustomers error")


    # def createAccount(
    #         # self,
    #         # api_id: str,
    #         # api_hash: str,
    #         # phone: str,
    #         # username: str,
    #         # host: Optional[str],
    #         # port: Optional[str],
    #         # public_key: Optional[str]
    # ):
    #     with app.app_context():
    #         if AccountModel.query.filter_by(username=self.username).first():
    #             response = databaseResponseModel(
    #                 status=False,
    #                 action="Create new account",
    #                 message="Account already created in database, unsuccessfully"
    #             )
    #             log.logger.warning(response)
    #             return response
    #         else:
    #             self.api_id = api_id
    #             self.api_hash = api_hash
    #             self.phone = phone
    #             self.username = username
    #             self.host = host
    #             self.port = port
    #             self.public_key = public_key
    #
    #             db.session.add(self)
    #             db.session.commit()
    #
    #             response = databaseResponseModel(
    #                 status=True,
    #                 action="Create new account",
    #                 message="Account created in database successfully"
    #             )
    #             log.logger.info(response)
    #             return response
    #
    # def updateAccount(
    #         self,
    #         api_id: Optional[str] = None,
    #         api_hash: Optional[str] = None,
    #         phone: Optional[str] = None,
    #         username: Optional[str] = None,
    #         host: Optional[str] = None,
    #         port: Optional[str] = None,
    #         public_key: Optional[str] = None
    # ):
    #     with app.app_context():
    #         account = AccountModel.query.filter_by(username=self.username).first()
    #         if account is not None:
    #             account.api_id = api_id if api_id is not None else account.api_id
    #             account.api_hash = api_hash if api_hash is not None else account.api_hash
    #             account.phone = phone if phone is not None else account.phone
    #             account.username = username if username is not None else account.username
    #             account.host = host if host is not None else account.host
    #             account.port = port if port is not None else account.port
    #             account.public_key = public_key if public_key is not None else account.public_key
    #
    #             account.session.commit()
    #
    #             response = databaseResponseModel(
    #                 status=True,
    #                 action="Update account",
    #                 message="Account updated, successfully"
    #             )
    #
    #             log.logger.info(response)
    #             return response
    #
    #         else:
    #             response = databaseResponseModel(
    #                 status=False,
    #                 action="Update account",
    #                 message="Account doesnt found, update unsuccessfully"
    #             )
    #             log.logger.warning(response)
    #             return response
    #
    # def deleteAccount(self):
    #     with app.app_context():
    #         if AccountModel.query.filter_by(username=self.username).first():
    #             AccountModel.query.filter_by(username=self.username).delete()
    #             db.session.commit()
    #             response = databaseResponseModel(
    #                 status=True,
    #                 action="Delete account",
    #                 message="Account deleted, successfully"
    #             )
    #             log.logger.info(response)
    #             return response
    #         else:
    #             response = databaseResponseModel(
    #                 status=False,
    #                 action="Delete account",
    #                 message="Account doesnt found, deleted unsuccessfully"
    #             )
    #             log.logger.warning(response)
    #             return response
