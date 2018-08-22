from flask_restful import Resource, reqparse
from rest_api.models.tracking import TrackingModel
from flask_jwt_extended import jwt_required

##############################################
#### Create tracking log ####################
##############################################
class TrackingCreate(Resource):

    tracking_parser = reqparse.RequestParser()
    tracking_parser.add_argument(
        "order_id", type=int, required=True, help="order_id cannot be blank."
    )
    tracking_parser.add_argument(
        "staff_id", type=int, required=True, help="staff_id cannot be blank."
    )    
    tracking_parser.add_argument(
        "user_id", type=int, required=False
    )
    tracking_parser.add_argument(
        "message", type=str, required=False, help="order_id cannot be blank."
    )

    @jwt_required
    def post(self):
        data = self.tracking_parser.parse_args()

        # TODO prevent duplicated post
        
        if not data['user_id']:
            user_id = 0
        else:
            user_id = data['user_id']

        trk_log = TrackingModel(data['message'], data['order_id'], data['staff_id'],user_id)
        trk_log.save_to_db()
        return {
            "message":"tracking log created succesfully."
        },200



##############################################
#### retrieve tracking log ####################
##############################################
class TrackingInfo(Resource):

    tracking_parser = reqparse.RequestParser()
    tracking_parser.add_argument(
        "trk_log_id", type=int, required=True, help="trk_log_id cannot be blank."
    )

    @jwt_required
    def post(self):
        data = self.tracking_parser.parse_args()
        trk_log = TrackingModel.find_by_id(data['trk_log_id'])

        if not trk_log:
            return {
                "message":"no tracking log with {} was found.".format(data["trk_log_id"])
            },400
        return trk_log.json(),200



##############################################
#### update tracking log ####################
##############################################
class TrackingUpdate(Resource):
    tracking_parser = reqparse.RequestParser()
    tracking_parser.add_argument(
        "trk_log_id", type=int, required=True, help="trk_log_id cannot be blank."
    )
    tracking_parser.add_argument(
        "order_id", type=int, required=True, help="order_id cannot be blank."
    )
    tracking_parser.add_argument(
        "staff_id", type=int, required=True, help="staff_id cannot be blank."
    )    
    tracking_parser.add_argument(
        "user_id", type=int, required=True, help="user_id cannot be blank."
    )
    tracking_parser.add_argument(
        "message", type=str, required=False, help="order_id cannot be blank."
    )

    @jwt_required
    def put(self):
        data = self.tracking_parser.parse_args()
        trk_log = TrackingModel.find_by_id(data['trk_log_id'])

        if not trk_log:
            return {
                "message":"no tracking log with {} was found.".format(data["trk_log_id"])
            },400
        
        trk_log.order_id = data['order_id']
        trk_log.staff_id = data['staff_id']
        trk_log.user_id = data['user_id']
        trk_log.message = data['message']
        trk_log.save_to_db()

        return {"message":"tracking log updated sucssesfully."},200


##############################################
#### delete tracking log ####################
##############################################
class TrackingDelete(Resource):
    tracking_parser = reqparse.RequestParser()
    tracking_parser.add_argument(
        "trk_log_id", type=int, required=True, help="trk_log_id cannot be blank."
    )

    @jwt_required
    def delete(self):
        data = self.tracking_parser.parse_args()
        trk_log = TrackingModel.find_by_id(data['trk_log_id'])

        if not trk_log:
            return {
                "message":"no tracking log with {} was found.".format(data["trk_log_id"])
            },400
        
        trk_log.delete_from_db()
        return {"message":"tracking log deleted."}, 200

