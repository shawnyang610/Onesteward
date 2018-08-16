from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired







class AddressCreateForm (FlaskForm):

    line1 = StringField("Line1", validators=[DataRequired()])
    line2 = StringField("Line2")
    city = StringField("City", validators=[DataRequired()])
    state= StringField("State", validators=[DataRequired()])
    zip = StringField("Zip Code", validators=[DataRequired()])


    submit = SubmitField("Save Address")

