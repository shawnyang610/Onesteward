from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from rest_api.models.staff import StaffModel
# from werkzeug.security import safe_str_cmp
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token,
#     jwt_refresh_token_required,
#     get_jwt_identity,
#     get_raw_jwt,
#     jwt_required
# )
# from blacklist import BLACKLIST


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

