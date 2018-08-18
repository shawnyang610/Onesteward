from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, PasswordField
from wtforms.validators import DataRequired
from rest_api.models.user import UserModel
from rest_api.models.staff import StaffModel
# from werkzeug.security import check_password_hash


class AuthLogin(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Login")

    def validate_username(self, username):
        if (not UserModel.find_by_name(username.data)) and (not StaffModel.find_by_name(username.data)):
            raise ValidationError("username doesn't exist.")
