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

from rest_api.models.jwt import RevokedTokenModel # noqa

@jwt.token_in_blacklist_loader
def is_blacklisted(decrypted_token):
    jti = decrypted_token["jti"]
    return RevokedTokenModel.is_jti_blacklisted(jti)

###########################
#### config api  ######
###########################
api = Api(app)

from rest_api.resources.jwt import TokenRefresh # noqa
api.add_resource(TokenRefresh, "/refresh")

from rest_api.resources.user import (
    UserRegister,
    UserAccountInfo,
    UserCloseAccount,
    UserUpdateInfo,
    UserLogin,
    UserLogoutAccess,
    UserLogoutRefresh
    )# noqa
api.add_resource(UserRegister, "/user/register")
api.add_resource(UserAccountInfo, "/user/info")
api.add_resource(UserCloseAccount, "/user/close_account")
api.add_resource(UserUpdateInfo, "/user/update")
api.add_resource(UserLogin, "/user/login")
api.add_resource(UserLogoutAccess, "/user/logout_access")
api.add_resource(UserLogoutRefresh, "/user/logout_refresh")

from rest_api.resources.company import (
    CompanyRegister, CompanyUpdateInfo, CompanyCloseAccount, CompanyAccountInfo
) # noqa
api.add_resource(CompanyRegister, "/company/register")
api.add_resource(CompanyAccountInfo, "/company/info")
api.add_resource(CompanyUpdateInfo, "/company/update")
api.add_resource(CompanyCloseAccount, "/company/close_account")

from rest_api.resources.staff import (
    StaffRegister,
    StaffAccountInfo,
    StaffUpdateInfo,
    StaffCloseAccount,
    StaffLogin,
    StaffLogoutAccess,
    StaffLogoutRefresh
) # noqa
api.add_resource(StaffRegister, "/staff/register")
api.add_resource(StaffAccountInfo, "/staff/info")
api.add_resource(StaffUpdateInfo, "/staff/update")
api.add_resource(StaffCloseAccount, "/staff/close_account")
api.add_resource(StaffLogin, "/staff/login")
api.add_resource(StaffLogoutAccess, "/staff/logout_access")
api.add_resource(StaffLogoutRefresh, "/staff/logout_refresh")

from rest_api.resources.order import (
    OrderCreate, OrderInfo, OrderUpdate, OrderDelete
) # noqa
api.add_resource(OrderCreate, "/order/new_order")
api.add_resource(OrderInfo, "/order/info")
api.add_resource(OrderUpdate, "/order/update")
api.add_resource(OrderDelete, "/order/delete")

from rest_api.resources.tracking import (
    TrackingCreate, TrackingInfo, TrackingUpdate, TrackingDelete
) # noqa
api.add_resource(TrackingCreate, "/tracking/new_post")
api.add_resource(TrackingInfo, "/tracking/info")
api.add_resource(TrackingUpdate, "/tracking/update")
api.add_resource(TrackingDelete, "/tracking/delete")

from rest_api.resources.address import (
    AddressCreate, AddressInfo, AddressUpdate, AddressDelete
) # noqa
api.add_resource (AddressCreate, "/address/new_address")
api.add_resource (AddressInfo, "/address/info")
api.add_resource (AddressUpdate, "/address/update")
api.add_resource (AddressDelete, "/address/delete")