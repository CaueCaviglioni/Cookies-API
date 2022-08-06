from db import db
import uuid

class SaleModel(db.Model):
    __tablename__ = "sales"

    # Relationships

    # Columns
    sale_id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer)
    uuid_sale = db.Column(db.String(36))
    quantity = db.Column(db.Integer)
    unity_price = db.Column(db.Float(precision = 2))
    total_price = db.Column(db.Float(precision = 2))
    is_money = db.Column(db.Boolean)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    customer = db.relationship("CustomerModel")

    cookie_id = db.Column(db.Integer, db.ForeignKey("cookies.cookie_id"))
    cookie = db.relationship("CookieModel")

    def __init__(self, order_id, uuid_sale, customer_id, cookie_id, quantity, unity_price, total_price, is_money):
        self.order_id = order_id
        self.uuid_sale = uuid_sale
        self.customer_id = customer_id
        self.cookie_id = cookie_id
        self.quantity = quantity
        self.unity_price = unity_price
        self.total_price = total_price
        self.is_money = is_money

    def json(self):
        return {
            "order_id": self.order_id,
            "uuid_sale": self.uuid_sale,
            "customer_id": self.customer_id,
            "cookie_id": self.cookie_id,
            "quantity": self.quantity,
            "unity_price": self.unity_price,
            "total_price": self.total_price,
            "is_money": self.is_money
            }

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid_sale = uuid).all()

    @classmethod
    def find_by_order_id(cls, order_id):
        return cls.query.filter_by(order_id = order_id).all()

    @classmethod
    def is_repeated(cls, customer_id, cookie_id):
        return cls.query.filter_by(customer_id = customer_id, cookie_id = cookie_id).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()