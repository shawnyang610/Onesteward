from flask import Blueprint, render_template, redirect, url_for, request
from rest_api.forms.auth import AuthLogin
from rest_api.models.user import UserModel
from rest_api.models.staff import StaffModel
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from rest_api.controls.auth import render_error_page_wrong_password

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login ():

    form = AuthLogin()

    if form.validate_on_submit():

        user = UserModel.find_by_name(form.username.data)
        staff = StaffModel.find_by_name(form.username.data)

        if staff and check_password_hash(staff.password_hash, form.password.data):
            login_user(staff)

        elif user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)

        else:
            return render_error_page_wrong_password()

        next = request.args.get("next")

        if not next:
            next = url_for("web.index")
        
        return redirect(next)

    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout ():
    logout_user()
    return redirect(url_for("web.index"))