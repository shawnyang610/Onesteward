from flask import Blueprint, render_template

staff_bp = Blueprint("staff", __name__)

@staff_bp.route("/register")
def staff_register():
    return render_template("staff_register.html")


@staff_bp.route("/login")
def staff_login():
    return render_template("staff_login.html")


@staff_bp.route("/info")
def staff_info():
    return render_template("staff_account.html")


@staff_bp.route("/update")
def staff_update():
    return render_template("staff_account.html")


@staff_bp.route("/close_account")
def staff_close_account():
    return render_template("staff_account.html")
