from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from rest_api.models.address import AddressModel







class AddressCreateForm (FlaskForm):

    line1 = StringField("Line1", validators=[DataRequired()])
    line2 = StringField("Line2")
    city = StringField("City", validators=[DataRequired()])
    state= StringField("State", validators=[DataRequired()])
    zip = StringField("Zip Code", validators=[DataRequired()])


    submit = SubmitField("Save Address")

