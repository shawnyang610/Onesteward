from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from rest_api.models.staff import StaffModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_raw_jwt
)
from rest_api.models.jwt import RevokedTokenModel


class StaffRegister(Resource):
    staff_parser = reqparse.RequestParser()
    staff_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )
    staff_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank"
    )
    staff_parser.add_argument(
        "company_id", type=int, required=True, help="company_id cannot be blank"
    )
    # @jwt_required
    def post(self):
        data = self.staff_parser.parse_args()
        staff = StaffModel.find_by_name(data["username"])
        if staff:
            return {
                "message":"a staff with the username '{}' already exists".format(data["username"])
            },400
        
        staff = StaffModel(
            data["username"],
            generate_password_hash(data["password"]),
            data["company_id"]
        )
        staff.save_to_db()

        return {
            "message":"staff created successfully."
        },200


class StaffAccountInfo(Resource):
    staff_parser = reqparse.RequestParser()
    staff_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )
    staff_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank"
    )
    # @jwt_required
    def post(self):
        data = self.staff_parser.parse_args()
        staff = StaffModel.find_by_name(data["username"])

        if not staff:
            return {
                "message":"staff with username '{}' doesn't exist.".format(data["username"])
            },404

        return staff.json(),200


class StaffUpdateInfo(Resource):

    staff_parser = reqparse.RequestParser()
    staff_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )
    staff_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank"
    )
    staff_parser.add_argument(
        "company_id", type=int, required=True, help="company_id cannot be blank"
    )

    # @jwt_required
    def put(self):
        data = self.staff_parser.parse_args()

        staff = StaffModel.find_by_name(data["username"])
        if not staff:
            return {
                "message":"staff with username '{}' doesn't exist.".format(data["username"])
            },404
        
        staff.company_id = data["company_id"]
        staff.save_to_db()
        return {
            "message":"staff info updated succesfully."
        },200
        

class StaffCloseAccount(Resource):
    staff_parser = reqparse.RequestParser()
    staff_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank"
    )
    staff_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank"
    )

    def delete(self):
        data = self.staff_parser.parse_args()

        staff = StaffModel.find_by_name(data["username"])
        if not staff:
            return {
                "message":"staff with username '{}' doesn't exist.".format(data["username"])
            },404
        staff.delete_from_db()
        return {
            "message":"staff deleted."
        }, 200


class StaffLogin(Resource):
    staff_parser = reqparse.RequestParser()
    staff_parser.add_argument(
        "username", type=str, required=True, help="username cannot be blank."
    )
    staff_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank."
    )

    def post(self):
        data = self.staff_parser.parse_args()
        staff = StaffModel.find_by_name(data["username"])

        if not staff:
            return {"message":"username does not exist."},404
        
        if check_password_hash(staff.password_hash, data["password"]):
            access_token = create_access_token(identity=data["username"])
            refresh_token = create_refresh_token(identity=data["username"])
            return {
                "message":"Logged in as {}".format(staff.name),
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        else:
            return {"message": "wrong credentials."}


class StaffLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti)
            revoked_token.save_to_db()
            return {"message":"Access Token has been revoked."},200
        except:
            return {"message": "Something went wrong"},500


class StaffLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti)
            revoked_token.save_to_db()
            return {"message":"Refresh Token has been revoked."},200
        except:
            return {"message":"Something went wrong"},500