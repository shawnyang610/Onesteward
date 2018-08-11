from flask_restful import Resource, reqparse
from rest_api.models.address import AddressModel

##############################
#### Create address ##########
##############################
class AddressCreate(Resource):
    adr_parser = reqparse.RequestParser()
    adr_parser.add_argument(
        "line1", type=str, required=True, help="line1 cannot be blank."
    )
    adr_parser.add_argument(
        "line2", type=str, required=False
    )
    adr_parser.add_argument(
        "city", type=str, required=True, help="city cannot be blank."
    )
    adr_parser.add_argument(
        "state", type=str, required=True, help="state cannot be blank."
    )
    adr_parser.add_argument(
        "zip", type = str, required=True, help="zip cannot be blank."
    )
    adr_parser.add_argument(
        "company_id", type=int,required=False
    )
    adr_parser.add_argument(
        "user_id", type=int,required=False
    )

    def post(self):
        data = self.adr_parser.parse_args()

        address = AddressModel(
            line1=data["line1"],
            line2=data["line2"],
            city=data["city"],
            state=data["state"],
            zip=data["zip"],
            company_id=data["company_id"] if data["company_id"] else 1, # 1 = not applicable
            user_id=data["user_id"] if data["user_id"] else 1 # 1=not applicable
        )
        address.save_to_db()
        return {"message":"address created sucsessfully."}



##############################
#### retrieve address ##########
##############################
class AddressInfo(Resource):
    adr_parser = reqparse.RequestParser()
    adr_parser.add_argument(
        "address_id", type=int, required=True, help="address_id cannot be blank."
    )

    def post(self):
        data = self.adr_parser.parse_args()

        address = AddressModel.find_by_id(data["address_id"])
        if not address:
            return {"message":"address with id {} not found".format(data["address_id"])},400
        return address.json(),200



##############################
#### Update address ##########
##############################

class AddressUpdate(Resource):
    adr_parser = reqparse.RequestParser()
    adr_parser.add_argument(
        "address_id", type=int, required=True, help="address_id cannot be blank."
    )
    adr_parser.add_argument(
        "line1", type=str, required=True, help="line1 cannot be blank."
    )
    adr_parser.add_argument(
        "line2", type=str, required=True, help="line2 cannot be blank."
    )
    adr_parser.add_argument(
        "city", type=str, required=True, help="city cannot be blank."
    )
    adr_parser.add_argument(
        "state", type=str, required=True, help="state cannot be blank."
    )
    adr_parser.add_argument(
        "zip", type = str, required=True, help="zip cannot be blank."
    )

    def put(self):
        data = self.adr_parser.parse_args()
        
        address = AddressModel.find_by_id(data["address_id"])
        if not address:
            return {"message":"address with id {} not found".format(data["address_id"])},400

        address.line1 = data["line1"]
        address.line2 = data["line2"]
        address.city = data["city"]
        address.state= data["state"]
        address.zip = data["zip"]
        address.save_to_db()

        return {"message":"address updated successfully."},200

##############################
#### delete address ##########
##############################
class AddressDelete(Resource):
    adr_parser = reqparse.RequestParser()
    adr_parser.add_argument(
        "address_id", type=int, required=True, help="address_id cannot be blank."
    )

    def delete(self):
        data = self.adr_parser.parse_args()

        address = AddressModel.find_by_id(data["address_id"])
        if not address:
            return {"message":"address with id {} not found".format(data["address_id"])},400
        
        address.delete_from_db()
        return {"message":"address deleted successfully."},200

