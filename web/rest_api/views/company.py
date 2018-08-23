from flask import Blueprint, render_template, url_for, redirect, request
from rest_api.forms.company import RegistrationForm, UpdateForm
from rest_api.models.company import CompanyModel
from rest_api.models.address import AddressModel
from flask_login import login_required, current_user
from rest_api.controls.auth import (
    is_admin,
    render_error_page_unauthorized_access,
    is_admin_or_company_admin_of_the_same_company)

company_bp = Blueprint("company", __name__)



@company_bp.route("/create", methods= ["GET", "POST"])
@login_required
def company_create():

    # only admin is allowed to add new companies
    if not is_admin(current_user):
        return render_error_page_unauthorized_access()

    form = RegistrationForm()

    if form.validate_on_submit():
        company = CompanyModel(
            name=form.company_name.data,
            email=form.email.data,
            phone=form.phone.data)
        company.save_to_db()

        address = AddressModel(
            line1=form.line1.data,
            line2=form.line2.data,
            city=form.city.data,
            state=form.state.data,
            zip=form.zip.data,
            company_id=company.id,
            user_id =1
        )
        address.save_to_db()

        return redirect(url_for("company.company_info"))

    return render_template("company_create.html", form = form)


@company_bp.route("/update/<int:company_id>", methods=["GET", "POST"])

def company_update(company_id):

    if not is_admin_or_company_admin_of_the_same_company(current_user, company_id):
        return render_error_page_unauthorized_access()

    form = UpdateForm()

    company = CompanyModel.find_by_id(company_id)

    if form.validate_on_submit():
        company.email = form.email.data
        company.phone = form.phone.data
        company.save_to_db()

        return redirect(url_for("company.company_info"))

    form.company_name.data = company.name
    form.email.data = company.email
    form.phone.data = company.phone
    return render_template("company_update.html", form = form)


# display a list of all the company names.
@company_bp.route("/info")
def company_info():

    page = request.args.get("page", 1, type=int)
    companies = CompanyModel.find_all().paginate(page = page, per_page=10)

    return render_template("company_info.html", companies = companies)


@company_bp.route("/close_account/<int:company_id>", methods=["GET","POST"])
@login_required
def company_close_account(company_id):
    if not is_admin():
        return render_error_page_unauthorized_access()

    company = CompanyModel.find_by_id(company_id)
    if company:
        company.delete_from_db()

    return redirect(url_for("company.company_info"))