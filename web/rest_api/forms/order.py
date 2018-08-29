from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, NumberRange, Length
from rest_api.models.order import OrderModel
from rest_api.controls.urcode_generator import decode_qrcode

class OrderCreateForm (FlaskForm):

    ur_code = StringField("Order Number", validators=[DataRequired()] )
    name = StringField("Service Type", validators=[DataRequired()])
    staff_id = IntegerField("Staff ID", validators=[DataRequired(), NumberRange()])
    submit = SubmitField("Save Order")

    def check_ur_code(self, ur_code):

        if OrderModel.find_by_ur_code(ur_code):
            raise ValidationError("Sorry, that Order Number already exists.")



class OrderUpdateForm (FlaskForm):

    name = StringField("Service Type", validators=[DataRequired()])
    staff_id = IntegerField("Staff ID", validators=[DataRequired()])
    submit = SubmitField("Update Order")


class OrderCheckStatusByNumberForm(FlaskForm):
    order_number = StringField("Order Number", validators=[NumberRange(), Length(min=3, max=30)], description="Order Number")
    submit = SubmitField("Search for Order")


    def validate_order_number(self, order_number):

        if not OrderModel.find_by_ur_code(order_number.data):
            raise ValidationError("no order found, please try again.")


class OrderCheckStatusByQRCodeForm(FlaskForm):
    qrcode_img = FileField ("Upload QR Code Image", validators=[DataRequired(),FileAllowed(["jpg","png"])],description="Select QR CODE Image", render_kw={"placeholder":"Select QR Code Image"})
    submit = SubmitField("Search")

    def validate_qrcode_img(self, qrcode_img):
        decoded_data = decode_qrcode(qrcode_img.data)
        if not isinstance(decoded_data, str):
            raise ValidationError("unable to read the QR Code")
        if not OrderModel.find_by_ur_code(decoded_data):
            raise ValidationError("no order found, please try again.")

