from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from rest_api.models.company import CompanyModel
from rest_api.models.address import AddressModel
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

#######################################
#### register new affiliated company ##
#######################################

class CompanyRegister(Resource):
    company_parser = reqparse.RequestParser()
    company_parser.add_argument(
        "company_name", type=str, required=True, help="company name cannot be blank."
    )
    company_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank."
    )
    company_parser.add_argument(
        "email", type=str, required=True, help="email cannot be blank."
    )
    company_parser.add_argument(
        "phone", type=str, required=True, help="phone cannot be blank."
    )
    company_parser.add_argument(
        "line1", type=str, required=True, help="line1 cannot be blank."
    )
    company_parser.add_argument(
        "line2", type=str
    )
    company_parser.add_argument(
        "city", type=str, required=True, help="city cannot be blank."
    )
    company_parser.add_argument(
        "state", type=str, required=True, help="state cannot be blank."
    )
    company_parser.add_argument(
        "zip", type=str, required=True, help="zipcode cannot be blank."
    )
    # register a new affiliated partner company
    # @jwt_required
    def post(self):
        data = self.company_parser.parse_args()
        company = CompanyModel.find_by_name(data["company_name"])
        if company:
            return {
                "message":"company with this name already exits."
            },400

        company = CompanyModel(
            data["company_name"],
            generate_password_hash(data["password"]),
            data["email"],
            data["phone"]
            )
        company.save_to_db()

        line2 = data["line2"]
        if not line2:
            line2=""
        address = AddressModel(
            line1=data["line1"],
            line2=line2,
            city=data["city"],
            state=data["state"],
            zip=data["zip"],
            company_id=company.id
        )
        address.save_to_db()

        return {
            "message":"company '{}' is created successfully.".format(data["company_name"])
        },200


############################################
#### close company account (soft delete)####
############################################

class CompanyCloseAccount(Resource):

    company_parser = reqparse.RequestParser()
    company_parser.add_argument(
        "company_name", type=str, required=True, help="company name cannot be blank."
    )
    company_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank."
    )

    def delete(self):
        data = self.company_parser.parse_args()
        company = CompanyModel.find_by_name(data["company_name"])
        if not company:
            return {
                "message":"company name:{} not found".format(data["company_name"])
                },404
        if not check_password_hash(company.password_hash, data["password"]):
            return {
                "message": "incorrect password."
            },401

        company.delete_from_db()
        return {
            "message":"company:{} deleted".format(data["company_name"])
            },200


############################################
#### update existing company account info  ####
############################################

class CompanyUpdateInfo(Resource):
    company_parser = reqparse.RequestParser()
    company_parser.add_argument(
        "company_name", type=str, required=True, help="company name cannot be blank."
    )
    company_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank."
    )
    company_parser.add_argument(
        "email", type=str, required=True, help="email cannot be blank."
    )
    company_parser.add_argument(
        "phone", type=str, required=True, help="phone cannot be blank."
    )

    # @jwt_required
    def put(self):
        data = self.company_parser.parse_args()
        company = CompanyModel.find_by_name(data["company_name"])
        if not company:
            return {
                "message":"company name: {} not found".format(data["company_name"])
            },404
        if not check_password_hash(company.password_hash, data["password"]):
            return {
                "message": "incorrect password."
            },401

        company.email = data["email"]
        company.phone = data["phone"]
        company.save_to_db()
        return {
            "message":"company info updated"
        },200


######################################################
#### retrieves all account info for a company  ####
######################################################
class CompanyAccountInfo(Resource):
    company_parser = reqparse.RequestParser()
    company_parser.add_argument(
        "company_name", type=str, required=True, help="company name cannot be blank."
    )
    company_parser.add_argument(
        "password", type=str, required=True, help="password cannot be blank."
    )
    # @jwt_required
    def post(self):
        data = self.company_parser.parse_args()
        company = CompanyModel.find_by_name(data["company_name"])
        if not company:
            return {
                "message":"company name: {} not found".format(data["company_name"])
            },404
        if not check_password_hash(company.password_hash, data["password"]):
            return{
                "message":"incorrect password."
            },401
        
        return company.json(),200

