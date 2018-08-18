from flask import Blueprint, render_template, redirect, url_for, request
from rest_api.forms.user import UserCreateForm
from rest_api.models.user import UserModel
from werkzeug.security import generate_password_hash
user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["GET", "POST"])
def user_register():

    form = UserCreateForm()

    if form.validate_on_submit():
        user = UserModel(
            hashed_password = generate_password_hash(form.password.data),
            name = form.username.data,
            email = form.email.data,
            phone = form.phone.data
        )
        user.save_to_db()
        return redirect(url_for("web.index"))

    return render_template("user_register.html", form=form)


# @user_bp.route("/login")
# def user_login():
#     return render_template("user_login.html")


@user_bp.route("/account")
def user_account():
    user_id = request.args.get("user_id", type=int)
    user = UserModel.find_by_id(user_id)
    return render_template("user_account.html", user)


@user_bp.route("/user_list")
def user_list ():
    page = request.args.get("page", 1, type=int)
    users = UserModel.find_all().paginate(page=page, per_page=5)

    return render_template("user_list.html", users=users)



# update and close account can all be done in account page using diff forms. 

@user_bp.route("/update")
def user_update():
    return render_template("user_account.html")


@user_bp.route("/close_account")
def user_close_account():
    return render_template("user_account.html")

