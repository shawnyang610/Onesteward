from flask import Blueprint, render_template, url_for, redirect
from rest_api.forms.company import RegistrationForm
from rest_api.models.company import CompanyModel

company_bp = Blueprint("company", __name__)



@company_bp.route("/create", methods= ["GET", "POST"])
def company_create():

    form = RegistrationForm()

    if form.validate_on_submit():
        company = CompanyModel(
            name=form.company_name.data,
            email=form.email.data,
            phone=form.phone.data)
        company.save_to_db()

        return redirect(url_for("company.company_info"))

    return render_template("company_create.html", form = form)


@company_bp.route("/update")
def company_update():


    return render_template("company_create.html")


@company_bp.route("/info")
def company_info():


    return render_template("company_info.html")


@company_bp.route("/close_account")
def company_close_account():


    return render_template("company_info.html")