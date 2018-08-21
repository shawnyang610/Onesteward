from flask import Blueprint, render_template, redirect, url_for, request
from rest_api.forms.staff import StaffCreateForm, StaffUpdateForm
from rest_api.models.staff import StaffModel
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from rest_api.controls.auth import (
    is_admin_or_company_admin_of_the_same_company,
    is_admin,
    is_company_admin,
    is_user,
    is_staff,
    render_error_page_unauthorized_access)

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/register", methods=["GET","POST"])
@login_required
def staff_register():
    
    if is_user(current_user) or is_staff(current_user):
        return render_error_page_unauthorized_access()

    form = StaffCreateForm()

    if form.validate_on_submit():
        if is_company_admin(current_user) and current_user.company_id !=form.company_id.data:
            return render_error_page_unauthorized_access()
        try:
            staff = StaffModel(
                form.username.data,
                form.role.data,
                generate_password_hash(form.password.data),
                form.company_id.data)

            staff.save_to_db()
        except:
            return {"message":"something went wrong"}
        return redirect(url_for("staff.staff_info"))

    return render_template("staff_register.html", form = form)


# @staff_bp.route("/login")
# def staff_login():
#     return render_template("staff_login.html")


@staff_bp.route("/info")
@login_required
def staff_info():
    
    page = request.args.get("page", 1, type=int)

    if is_user(current_user):
        return render_error_page_unauthorized_access()
    
    if is_admin(current_user):
        staffs= StaffModel.find_all()
    elif is_company_admin(current_user) or is_staff(current_user):
        staffs= StaffModel.find_by_company_id(current_user.company_id)

    staffs = staffs.paginate(page=page, per_page=5)

    return render_template("staff_info.html", staffs=staffs)


@staff_bp.route("/update/<int:staff_id>", methods=["GET","POST"])
def staff_update(staff_id):

    staff = StaffModel.find_by_id(staff_id)

    form = StaffUpdateForm()

    if form.validate_on_submit():
        staff.role =  form.role.data
        staff.password_hash = generate_password_hash(form.password.data)
        staff.company_id = form.company_id.data
        staff.save_to_db()
        return redirect(url_for("staff.staff_info"))

    form.role.data = staff.role
    form.company_id.data = staff.company_id

    return render_template("staff_update.html", form=form, staff=staff)

@staff_bp.route("/close_account/<int:staff_id>", methods=["GET","POST"])
def staff_close_account(staff_id):

    staff = StaffModel.find_by_id(staff_id)

    staff.delete_from_db()

    return redirect(url_for("staff.staff_info"))

@staff_bp.route("/workspace")
def staff_workspace():

    return render_template("staff_workspace.html")