from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)
from blacklist import BLACKLIST


class Order(Resource):

    # allow anyone with QR code to view current order tracking info
    # detailed information for logged in users
    @jwt_optional
    def get(self):
        pass

    # allow staff to post new order
    @jwt_required
    def post(self):
        pass

    # allow staff to delete existing order (logical deletion)
    @jwt_required
    def delete(self):
        pass

    # allow staff to update existing order info.(update tracking)
    @jwt_required
    def put(self):
        pass
