from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_raw_jwt,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
# from blacklist import BLACKLIST
from rest_api.models.user import UserModel
from rest_api.models.jwt import RevokedTokenModel




class UserAccountInfo(Resource):

    user_parser = reqparse.RequestParser()
    user_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )

    @jwt_required
    def post(self):
        data = self.user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])

        if not user:
            return {"message":"user:{} not found".format(data["username"])},404

        # auth group: user account owner, admin
        identity = get_jwt_identity()

        if identity["auth_level"] == "user" and identity["id"] != user.id:
            return {"message":"unauthorized access, user is only allowed to view his/her own account info"}, 500

        if identity["auth_level"] == "staff":
            return {"message":"unauthorized access for staff."},500


        return user.json(),200



class UserCloseAccount(Resource):

    user_parser = reqparse.RequestParser()
    user_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )

    @jwt_required
    def delete(self):
        data = self.user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])

        if not user:
            return {"message":"user:{} not found".format(data["username"])},404

        # auth group: user account owner, admin
        # all staffs and user with wrong id are unauthorized
        identity = get_jwt_identity()
        if identity["auth_level"] == "staff" or (
            identity["auth_level"] == "user" and identity["id"] != user.id):
            return {"message":"unauthorized access"},500 

        # authorized: admin, user account owner

        try:
            user.delete_from_db()
            return {"message":"user:{} deleted".format(data["username"])},200
        except:
            return {"message":"something went wrong"}


class UserUpdateInfo(Resource):

    user_parser = reqparse.RequestParser()
    user_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )
    user_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank"
    )
    user_parser.add_argument(
        "email", type=str, required=True, help="email cannot be blank"
    )

    @jwt_required
    def put(self):
        data = self.user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])

        if not user:
            return {"message":"user:{} not found".format(data["username"])},404

        # auth group: user account owner, admin
        # all staffs are user with wrong id are unauthorized
        identity = get_jwt_identity()
        if identity["auth_level"] == "staff" or (
            identity["auth_level"] == "user" and identity["id"] != user.id):
            return {"message":"unauthorized access"},500 

        # authorized: admin, user account owner

        user.email = data["email"]

        try:
            user.save_to_db()
            return {"message":"user info updated succesfully."},200
        except:
            return {"message":"something went wrong."}


class UserRegister(Resource):

    user_parser = reqparse.RequestParser()
    user_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )
    user_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank"
    )
    user_parser.add_argument(
        "email", type=str, required=True, help="email cannot be blank"
    )

    def post(self):
        data = self.user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])
        if user:
            return {
                "message":"username:already exists"
            }, 400

        user = UserModel(generate_password_hash(data["password"]), data["username"],data["email"])
        try:
            user.save_to_db()
            identity = {
                "auth_level":"user",
                "id":user.id
            }
            access_token = create_access_token(identity=identity)
            refresh_token= create_refresh_token(identity=identity)
            return {
                "message":"User created successfully.",
                "access_token":access_token,
                "refresh_token":refresh_token
                },201
        except:
            return {"message":"something went wrong."},500


class UserLogin(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank."
    )
    user_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank."
    )

    def post(self):
        data = self.user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])

        if not user:
            return {"message":"username does not exist."},404
        
        if check_password_hash(user.password_hash, data["password"]):
            identity = {
                "auth_level":"user",
                "id":user.id
            }
            access_token = create_access_token(identity=identity, fresh=True)
            refresh_token = create_refresh_token(identity=identity)
            return {
                "message":"Logged in as {}".format(user.name),
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        else:
            return {"message": "wrong credentials."}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti)
            revoked_token.save_to_db()
            return {"message":"Access Token has been revoked."},200
        except:
            return {"message": "Something went wrong"},500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti)
            revoked_token.save_to_db()
            return {"message":"Refresh Token has been revoked."},200
        except:
            return {"message":"Something went wrong"},500


