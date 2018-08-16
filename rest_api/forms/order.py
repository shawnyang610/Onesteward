from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, NumberRange
from rest_api.models.order import OrderModel

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
