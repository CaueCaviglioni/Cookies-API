import uuid
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
from models.sale import SaleModel

class Sale(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id", type = int)
    parser.add_argument("cookie_id", type = int)
    parser.add_argument("quantity", type = float)
    parser.add_argument("unity_price", type = float)
    parser.add_argument("is_money", type = bool)

    #@jwt_required()
    #def get(self, uuid_sale):
        #sale = SaleModel.find_by_uuid(uuid_sale)
        #if sale:
            #return {"customers": [sale.json() for sale in SaleModel.query.filter_by(uuid_sale = uuid_sale).all()]}
        #return {"message": "Sale not found"}, 404

    #@jwt_required(fresh = True)
    def delete(self, uuid_sale):
        sale = SaleModel.find_by_uuid(uuid_sale)
        if sale:
            sale.delete_from_db()

        return {"message": "Sale deleted."}

    #@jwt_required(fresh = True)
    def patch(self, uuid_sale):
        data = Sale.parser.parse_args()

        sale = SaleModel.find_by_uuid(uuid_sale)

        if sale:
            if data["customer_id"]:
                sale.customer_id = data["customer_id"]
            if data["cookie_id"]:
                sale.cookie_id = data["cookie_id"]
            if data["quantity"]:
                sale.quantity = data["quantity"]
            if data["unity_price"]:
                sale.unity_price = data["unity_price"]
            if data["is_money"]:
                sale.is_money = data["is_money"]

            sale.save_to_db()

            return sale.json()

        return {"message": f"There is no such sale in the database."}


class SaleList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("order_id", type = int, required = True, help = "This field cannot be blank.")
    parser.add_argument("customer_id", type = int, required = True, help = "This field cannot be blank.")
    parser.add_argument("cookie_id", type = int, required = True, help = "This field cannot be blank.")
    parser.add_argument("quantity", type = float, required = True, help = "This field cannot be blank.")
    parser.add_argument("unity_price", type = float, required = True, help = "This field cannot be blank.")
    parser.add_argument("total_price", type = float)
    parser.add_argument("is_money", type = bool, required = True, help = "This field cannot be blank.")

    #@jwt_required(fresh = True)
    def get(self):
        return {"sales": [sale.json() for sale in SaleModel.query.all()]}

    #@jwt_required()
    def post(self):
        data = SaleList.parser.parse_args()

        if SaleModel.find_by_order_id(data["order_id"]):
            if SaleModel.is_repeated(data["customer_id"], data["cookie_id"]):
                return {"message": "This order already exists"}, 400

        data["uuid_sale"] = str(uuid.uuid4())
        sale = SaleModel(**data)

        try:
            sale.save_to_db()
        except:
            return {"message": "An error occurred inserting the sale."}, 500

        return sale.json(), 201