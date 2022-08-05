import pymysql
from flask import Flask, request
from flask_restful import Api
#from flask_jwt_extended import JWTManager

from database_conn import secrets

from resources.cookie import Cookie, CookieList
from resources.customer import Customer, CustomerList
#from resources.user import UserLogin, TokenRefresh
from db import db

# Pega chaves de acesso para a conexão com o banco de dados
SECRET_KEY = secrets.get("SECRET_KEY")
DATABASE_USER = secrets.get("DATABASE_USER")
DATABASE_NAME = secrets.get("DATABASE_NAME")
DATABASE_PASSWORD = secrets.get("DATABASE_PASSWORD")
DATABASE_PORT = secrets.get("DATABASE_PORT")

# Inicia o app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost/{DATABASE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPETIONS"] = True
app.secret_key = SECRET_KEY
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

#jwt = JWTManager(app)

api.add_resource(CookieList, "/cookies")
api.add_resource(CustomerList, "/customers")
api.add_resource(Cookie, "/cookies/<string:name>")
api.add_resource(Customer, "/customers/<string:uuid_customer>")
#api.add_resource(UserLogin, "/login")
#api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug = True)