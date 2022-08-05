from db import db
import uuid

class CookieModel(db.Model):
    __tablename__ = "cookies"

    cookie_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float(precision = 2))

    #receipt = db.relationship("ReceiptModel", lazy = "dynamic")

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {
            "name": self.name,
            "price": self.price
            }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()