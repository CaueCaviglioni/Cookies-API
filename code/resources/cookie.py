from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required
from models.cookie import CookieModel

class Cookie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type = str)
    parser.add_argument("price", type = float)

    #@jwt_required()
    def get(self, name):
        cookie = CookieModel.find_by_name(name)
        if cookie:
            return cookie.json()
        return {"message": "Cookie not found"}, 404

    #@jwt_required(fresh = True)
    def delete(self, name):
        cookie = CookieModel.find_by_name(name)
        if cookie:
            cookie.delete_from_db()

        return {"message": "Cookie deleted."}

    #@jwt_required(fresh = True)
    def patch(self, name):
        data = Cookie.parser.parse_args()

        cookie = CookieModel.find_by_name(name)

        if cookie:
            if data["name"]:
                cookie.name = data["name"]
            if data["price"]:
                cookie.price = data["price"]

            cookie.save_to_db()

            return cookie.json()

        return {"message": f"There is no cookie with that flavour {name}."}


class CookieList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type = str)
    parser.add_argument("price", type = float)

    #@jwt_required(fresh = True)
    def get(self):
        return {"cookies": [cookie.json() for cookie in CookieModel.query.all()]}

    #@jwt_required()
    def post(self):
        data = Cookie.parser.parse_args()

        if CookieModel.find_by_name(data["name"]):
            name = data["name"]
            return {"message": f"A cookie with that flavour '{name}' already exists."}, 400

        cookie = CookieModel(**data)

        try:
            cookie.save_to_db()
        except:
            return {"message": "An error occurred inserting the cookie."}, 500

        return cookie.json(), 201
