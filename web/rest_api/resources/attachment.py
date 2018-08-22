from flask_restful import Resource, reqparse # noqa
from rest_api.models.attachment import AttachmentModel # noqa
from flask_jwt_extended import jwt_required

# TODO

##############################################
#### Create Attachment ####################
##############################################
class TrackingCreate(Resource):

    @jwt_required
    def post(self):
        pass



##############################################
#### retrieve attachment ####################
##############################################
class TrackingInfo(Resource):

    @jwt_required
    def post(self):
        pass



##############################################
#### update attachment ####################
##############################################
class TrackingUpdate(Resource):

    @jwt_required
    def put(self):
        pass


##############################################
#### delete attachment ####################
##############################################
class TrackingDelete(Resource):

    @jwt_required
    def delete(self):
        pass