from db import db
import uuid

class CustomerModel(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key = True)
    uuid_customer = db.Column(db.String(36))
    name = db.Column(db.String(200))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(200))
    is_vip = db.Column(db.String(100))

    #receipt = db.relationship("ReceiptModel", lazy = "dynamic")

    def __init__(self, uuid_customer, name, telephone, email, is_vip):
        self.uuid_customer = uuid_customer
        self.name = name
        self.telephone = telephone
        self.email = email
        self.is_vip = is_vip

    def json(self):
        return {
            "uuid_customer": self.uuid_customer,
            "name": self.name,
            "telephone": self.telephone,
            "email": self.email,
            "is_vip": self.is_vip
            }

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid_customer = uuid).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()