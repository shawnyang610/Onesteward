from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email

# from flask_login import current_user
from rest_api.models.company import CompanyModel







class RegistrationForm (FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired()])

    line1 = StringField("Line1", validators=[DataRequired()])
    line2 = StringField("Line2")
    city = StringField("City", validators=[DataRequired()])
    state= StringField("State", validators=[DataRequired()])
    zip = StringField("Zip Code", validators=[DataRequired()])


    submit = SubmitField("Register!")

    def validate_company_name(self, company_name):

        if CompanyModel.find_by_name(company_name):
            raise ValidationError("Company name already exists.")


    def validate_email(self, email):
        if CompanyModel.find_by_email(email):
            raise ValidationError("Email already exists.")


class UpdateForm (FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired()])


    submit = SubmitField("Update")
