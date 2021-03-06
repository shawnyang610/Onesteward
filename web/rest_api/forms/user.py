from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email
from rest_api.models.user import UserModel


class UserCreateForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()], description="Username")
    email = StringField("Email", validators=[DataRequired(),Email()], description="Email")
    phone = StringField("Phone", description="Phone")
    password = PasswordField("password", validators=[DataRequired(),EqualTo("pass_confirm", message="password must match!")], description="Password")
    pass_confirm =  PasswordField("confirm password", validators=[DataRequired()], description="Confirm Password")
    submit = SubmitField("Register")

    def validate_username(self, username):
        if UserModel.find_by_name(username.data):
            raise ValidationError("your username has been registered.")

    def validate_email(self, email):
        if UserModel.find_by_email(email.data):
            raise ValidationError("your email has been registered.")

class UserUpdateForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()], description="Email")
    phone = StringField("Phone", description="Phone")
    password = PasswordField("password", validators=[DataRequired(),EqualTo("pass_confirm", message="password must match!")], description="Password")
    pass_confirm =  PasswordField("confirm password", validators=[DataRequired()], description="Confirm Password")
    submit = SubmitField("Update")