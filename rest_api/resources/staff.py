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
# from blacklist import BLACKLIST


class Staff(Resource):


    @jwt_required
    def get(self):
        pass

    @jwt_required
    def post(self):
        pass


    @jwt_required
    def put(self):
        pass
