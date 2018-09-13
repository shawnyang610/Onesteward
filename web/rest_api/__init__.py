from os.path import abspath, dirname, join
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

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

app.config['POSTGRES_USER'] = "shawn"
app.config["POSTGRES_DEFAULT_USER"] = "postgres"
app.config["POSTGRES_PASSWORD"] = "my_password"
app.config["POSTGRES_DB"]="onesteward-db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ join(basedir, "data.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+ app.config['POSTGRES_USER']+":"+app.config["POSTGRES_PASSWORD"]+"@postgres:5432/"+app.config["POSTGRES_DB"]
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

# TODO
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    pass

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

######################################################
#### web #############################################
######################################################



########################################
#### login ############################
#######################################

from rest_api.models.staff import StaffModel # noqa
from rest_api.models.user import UserModel # noqa

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    role = user_id.split("_")[0]
    _id = user_id.split("_")[1]
    if role == "staff":
        return StaffModel.find_by_id(int(_id))
    if role == "user":
        return UserModel.find_by_id(int(_id))
    # return StaffModel.find_by_id(user_id)


###################################################
#### add onesteward as first company ##############
#### add admin as super user         ##############
###################################################
# from rest_api.models.company import CompanyModel # noqa
# from rest_api.models.staff import StaffModel    # noqa
# from rest_api.models.user import UserModel # noqa
# @app.before_first_request
# def add_super_company_user():

#     first_company = CompanyModel.find_by_name("OneSteward")

#     if not first_company:
#         first_company = CompanyModel(
#             "OneSteward",
#             "admin@onesteward.com",
#             "555-555-5555")
#         first_company.save_to_db()

#     first_staff = StaffModel.find_by_name("admin")
#     if not first_staff:
#         first_staff = StaffModel(
#             "admin",
#             "admin",
#             generate_password_hash("admin_password"),
#             first_company.id)

#         first_staff.save_to_db()

#     first_user = UserModel.find_by_name("NA")
#     if not first_user:
#         first_user = UserModel(
#             generate_password_hash("admin_password"),
#             name = "NA",
#             email="NA")

#         first_user.save_to_db()


########################################
#### blueprint #########################
########################################

from rest_api.views.home import home_bp # noqa
app.register_blueprint(home_bp)

from rest_api.views.user import user_bp # noqa
app.register_blueprint(user_bp, url_prefix="/web/user")

from rest_api.views.staff import staff_bp # noqa
app.register_blueprint(staff_bp, url_prefix="/web/staff")

from rest_api.views.order import order_bp # noqa
app.register_blueprint(order_bp, url_prefix="/web/order")

from rest_api.views.address import address_bp # noqa
app.register_blueprint(address_bp, url_prefix="/web/address")

from rest_api.views.tracking_log import trk_log_bp # noqa
app.register_blueprint(trk_log_bp, url_prefix="/web/tracking_log")

from rest_api.views.company import company_bp # noqa
app.register_blueprint(company_bp, url_prefix="/web/company")

from rest_api.views.post import post_bp # noqa
app.register_blueprint(post_bp, url_prefix="/web/post")

from rest_api.views.admin import admin_bp # noqa
app.register_blueprint(admin_bp, url_prefix="/web/admin")

from rest_api.views.auth import auth_bp # noqa
app.register_blueprint(auth_bp)
