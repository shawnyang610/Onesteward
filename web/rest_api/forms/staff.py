from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from rest_api.models.staff import StaffModel


class StaffCreateForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    role = StringField("role", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(),EqualTo("pass_confirm", message="password must match!")])
    pass_confirm =  PasswordField("confirm password", validators=[DataRequired()])
    company_id = IntegerField("company ID", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if StaffModel.find_by_name(field.data):
            raise ValidationError("your username has been registered already.")



class StaffUpdateForm(FlaskForm):

    role = StringField("role", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(),EqualTo("pass_confirm", message="password must match!")])
    pass_confirm =  PasswordField("confirm password", validators=[DataRequired()])
    company_id = IntegerField("company ID", validators=[DataRequired()])
    submit = SubmitField("Update")
