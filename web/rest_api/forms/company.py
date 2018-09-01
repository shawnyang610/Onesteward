from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email

# from flask_login import current_user
from rest_api.models.company import CompanyModel







class RegistrationForm (FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()], description="Company Name")
    email = StringField("Email", validators=[DataRequired(), Email()], description="Email")
    phone = StringField("Phone", validators=[DataRequired()], description="Phone")

    line1 = StringField("Line1", validators=[DataRequired()], description="Line 1")
    line2 = StringField("Line2", description="Line 2")
    city = StringField("City", validators=[DataRequired()], description="City")
    state= StringField("State", validators=[DataRequired()], description="State")
    zip = StringField("Zip Code", validators=[DataRequired()], description="Zip")
    submit = SubmitField("Register!")

    def validate_company_name(self, company_name):

        if CompanyModel.find_by_name(company_name.data):
            raise ValidationError("Company name already exists.")


    def validate_email(self, email):
        if CompanyModel.find_by_email(email.data):
            raise ValidationError("Email already exists.")


class UpdateForm (FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()], description="Company Name")
    email = StringField("Email", validators=[DataRequired(), Email()], description="Email")
    phone = StringField("Phone", validators=[DataRequired()], description="Phone")


    submit = SubmitField("Update")
