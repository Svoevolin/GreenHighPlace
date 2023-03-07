from app.config import db, app

# import os,sys
# sys.path.insert(1, os.path.join(sys.path[0], '../'))
# from config import app, db

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    chatId = db.Column(db.BigInteger, nullable=False)
    def __repr__(self):
        return f'{self.id}-#-#-{self.chatId}'
def addAdmin(chatId: int):
    try:
        with app.app_context():
            if Admin.query.filter_by(chatId=chatId).first():
                return 0
            else:
                admin = Admin(chatId=chatId)
                db.session.add(admin)
                db.session.commit()

            return 1
    except Exception as e:
        return print(e, "\naddAdmin error")

def getAdmins():
    try:
        with app.app_context():

            return Admin.query.filter(Admin.id is not None).all()

    except Exception as e:
        return print(e, "\ngetAllActiveOrders error")
def checkAdmin(chatId: int):
    try:
        with app.app_context():
            if Admin.query.filter_by(chatId=chatId).first():
                return True
            else:
                return False
    except Exception as e:
        return print(e, "\ncheckAdmin error")

