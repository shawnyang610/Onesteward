from flask_restful import Resource, reqparse
from rest_api.models.order import OrderModel
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


########################################
#### allow staff to post new order #####
########################################
class OrderCreate(Resource):
    order_parser = reqparse.RequestParser()
    order_parser.add_argument(
        "ur_code", type = str, required=True, help="ur_code cannot be blank."
    )
    order_parser.add_argument(
        "order_name", type = str, required=True, help="order_name cannot be blank."
    )
    order_parser.add_argument(
        "staff_id", type = str, required=True, help="staff_id cannot be blank."
    )

    # @jwt_required
    def post(self):
        data = self.order_parser.parse_args()

        order = OrderModel.find_by_ur_code(data["ur_code"])

        if order:
            return {
                "message":"order with ur_code {} already exists.".format(data["ur_code"])
            }, 400
        
        order = OrderModel(
            data["ur_code"],
            data["order_name"],
            data["staff_id"]
        )

        order.save_to_db()
        return {"message":"order created succesfully."},200

####################################################################
#### allow anyone with QR code to view current order tracking info #
#### detailed information for logged in users                      #
####################################################################
class OrderInfo(Resource):

    order_parser = reqparse.RequestParser()
    order_parser.add_argument(
        "ur_code", type = str, required=True, help="ur_code cannot be blank."
    ) 
    # @jwt_optional
    def post(self):
        data = self.order_parser.parse_args()

        order = OrderModel.find_by_ur_code(data["ur_code"])

        if not order:
            return {"message":"order with ur_code{} doen not exist.".format(data['ur_code'])},404
        
        # TODO 
        # if with partial permission


        # if with full permission
        return order.json(), 200




##################################################
#### update order    ############################
#################################################
class OrderUpdate(Resource):
    order_parser = reqparse.RequestParser()
    order_parser.add_argument(
        "ur_code", type = str, required=True, help="ur_code cannot be blank."
    )
    order_parser.add_argument(
        "order_name", type = str, required=True, help="order_name cannot be blank."
    )
    order_parser.add_argument(
        "staff_id", type = str, required=True, help="staff_id cannot be blank."
    )
    # user_id =0 by default is annonymous
    order_parser.add_argument(
        "user_id", type = str, required=True, help="staff_id cannot be blank."
    )
    # @jwt_required
    def put(self):
        data = self.order_parser.parse_args()
        
        order = OrderModel.find_by_ur_code(data["ur_code"])

        if not order:
            return {"message":"order with ur_code{} doen not exist.".format(data['ur_code'])},404
        
        order.name = data['order_name']
        order.staff_id = data['staff_id']
        order.user_id = data['user_id']
        order.save_to_db()
        return {"message":"order info updated succesfully."},200

#################################################
#### soft delete order ########################
################################################
class OrderDelete(Resource):
    order_parser = reqparse.RequestParser()
    order_parser.add_argument(
        "ur_code", type = str, required=True, help="ur_code cannot be blank."
    )
    # @jwt_required
    def delete(self):
        data = self.order_parser.parse_args()

        order = OrderModel.find_by_ur_code(data['ur_code'])

        if not order:
            return {"message":"order with ur_code{} doen not exist.".format(data['ur_code'])},404
        
        order.delete_from_db()

        return {"message":"order deleted succesfully."},200