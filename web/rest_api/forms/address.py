from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired







class AddressCreateForm (FlaskForm):

    line1 = StringField("Line1", validators=[DataRequired()], description="Line 1")
    line2 = StringField("Line2", description="Line 2")
    city = StringField("City", validators=[DataRequired()], description="City")
    state= StringField("State", validators=[DataRequired()], description="State")
    zip = StringField("Zip Code", validators=[DataRequired()], description="Zip")


    submit = SubmitField("Save Address")

