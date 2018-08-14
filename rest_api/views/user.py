from flask import Blueprint, render_template

user_bp = Blueprint("user", __name__)

@user_bp.route("/register")
def user_register():
    return render_template("user_register.html")


# @user_bp.route("/login")
# def user_login():
#     return render_template("user_login.html")


@user_bp.route("/account")
def user_account():
    return render_template("user_account.html")




# update and close account can all be done in account page using diff forms. 

@user_bp.route("/update")
def user_update():
    return render_template("user_account.html")


@user_bp.route("/close_account")
def user_close_account():
    return render_template("user_account.html")

