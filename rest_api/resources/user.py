from flask_restful import Resource, reqparse
# from werkzeug.security import safe_str_cmp
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token,
#     jwt_refresh_token_required,
#     get_jwt_identity,
#     get_raw_jwt,
#     jwt_required
# )
from werkzeug.security import generate_password_hash, check_password_hash
# from blacklist import BLACKLIST
from rest_api.models.user import UserModel




class UserAccountInfo(Resource):

    user_parser = reqparse.RequestParser()
    user_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )

    # @jwt_required
    # get user info
    def post(self):
        data = self.user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])
        if user:
            return user.json(),200
        return {"message":"user:{} not found".format(data["username"])},404



class UserCloseAccount(Resource):

    user_parser = reqparse.RequestParser()
    user_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )

    # @jwt_required
    def delete(self):
        data = self.user_parser.parse_args()
        user = UserModel.find_by_name(data["username"])
        if not user:
            return {"message":"user:{} not found".format(data["username"])},404
        user.delete_from_db()
        return {"message":"user:{} deleted".format(data["username"])},200


class UserUpdateInfo(Resource):

    pass

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
        user.save_to_db()
        return {"message":"User created successfully."},201


