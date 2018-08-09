from os.path import abspath, dirname, join
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


###########################
#### config flask app ####
###########################
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'myappsecretkey'

###########################
#### config database ######
##########################
basedir = abspath(dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app, db)


########################
#### config jwt ########
#######################
app.config["JWT_SECRET_KEY"] = "myjwtsecretkey"
app.config["JWT_BLACKLIST_ENABLED"] =True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
jwt = JWTManager(app)


###########################
#### config api  ######
###########################
from rest_api.resources.user import (
    UserRegister, UserAccountInfo, UserCloseAccount, UserUpdateInfo
    )# noqa
from rest_api.resources.company import (
    CompanyRegister, CompanyUpdateInfo, CompanyCloseAccount, CompanyAccountInfo
) # noqa
api = Api(app)

api.add_resource(UserRegister, "/user/register")
api.add_resource(UserAccountInfo, "/user/info")
api.add_resource(UserCloseAccount, "/user/close_account")
api.add_resource(UserUpdateInfo, "/user/update")

api.add_resource(CompanyRegister, "/company/register")
api.add_resource(CompanyAccountInfo, "/company/info")
api.add_resource(CompanyUpdateInfo, "/company/update")
api.add_resource(CompanyCloseAccount, "/company/close_account")
