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


class Company(Resource):

    # return all orders under the selected company
    @jwt_required
    def get(self):
        pass

    # register a new affiliated partner company
    @jwt_required
    def post(self):
        pass

    # mark an existing company as deleted (logical deletion)
    @jwt_required
    def delete(self):
        pass

    # update existing partner company's information
    @jwt_required
    def put(self):
        pass
