import uuid
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
from models.customer import CustomerModel

class Customer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type = str)
    parser.add_argument("telephone", type = str)
    parser.add_argument("email", type = str)
    parser.add_argument("is_vip", type = str)

    #@jwt_required()
    def get(self, uuid_customer):
        customer = CustomerModel.find_by_uuid(uuid_customer)
        if customer:
            #return customer.json()
            return {"customers": [customer.json() for customer in CustomerModel.query.filter_by(uuid_customer = uuid_customer).all()]}
        return {"message": "Customer not found"}, 404

    #@jwt_required(fresh = True)
    def delete(self, uuid_customer):
        customer = CustomerModel.find_by_uuid(uuid_customer)
        if customer:
            customer.delete_from_db()

        return {"message": "Customer deleted."}

    #@jwt_required(fresh = True)
    def patch(self, uuid_customer):
        data = Customer.parser.parse_args()

        customer = CustomerModel.find_by_uuid(uuid_customer)

        if customer:
            if data["name"]:
                customer.name = data["name"]
            if data["telephone"]:
                customer.telephone = data["telephone"]
            if data["email"]:
                customer.email = data["email"]
            if data["is_vip"]:
                customer.is_vip = data["is_vip"]

            customer.save_to_db()

            return customer.json()

        return {"message": f"There is no such customer in the database."}


class CustomerList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type = str, required = True, help = "This field cannot be blank.")
    parser.add_argument("telephone", type = str)
    parser.add_argument("email", type = str)
    parser.add_argument("is_vip", type = str, required = True, help = "This field cannot be blank.")

    #@jwt_required(fresh = True)
    def get(self):
        return {"customers": [customer.json() for customer in CustomerModel.query.all()]}

    #@jwt_required()
    def post(self):
        data = CustomerList.parser.parse_args()
        data["uuid_customer"] = str(uuid.uuid4())

        #if CustomerModel.fin(data["uuid_customer"]):
           #name = data["name"]
            #return {"message": f"A cookie with that flavour '{name}' already exists."}, 400

        customer = CustomerModel(**data)

        try:
            customer.save_to_db()
        except:
            return {"message": "An error occurred inserting the customer."}, 500

        return customer.json(), 201