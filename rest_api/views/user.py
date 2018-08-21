from flask import Blueprint, render_template, redirect, url_for, request
from rest_api.forms.user import UserCreateForm, UserUpdateForm
from rest_api.models.user import UserModel
from werkzeug.security import generate_password_hash
user_bp = Blueprint("user", __name__)
from flask_login import login_required, current_user
from rest_api.controls.auth import(
    is_admin,
    is_company_admin,
    is_staff,
    is_user,
    render_error_page_unauthorized_access
)

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
@login_required
def user_account():

    if is_user(current_user):
        user_id = current_user.id

    else:
        user_id = request.args.get("user_id", type=int)
    
    user = UserModel.find_by_id(user_id)
    return render_template("user_account.html", user=user)


@user_bp.route("/user_list")
@login_required
def user_list ():

    # no access to users(customers)
    if is_user(current_user):
        return render_error_page_unauthorized_access()

    # admin sees all users
    if is_admin(current_user):
        users = UserModel.find_all()
    # company_admin and staff sees all users of their company
    if is_company_admin or is_staff:
        pass

    page = request.args.get("page", 1, type=int)
    users = users.paginate(page=page, per_page=5)

    return render_template("user_list.html", users=users)



# update and close account can all be done in account page using diff forms. 

@user_bp.route("/update", methods=["GET","POST"])
@login_required
def user_update():
    if is_staff(current_user) or is_company_admin(current_user):
        return render_error_page_unauthorized_access()
    if is_user(current_user):
        user_id = current_user.id
    elif is_admin(current_user):
        user_id = request.args.get("user_id")

    user = UserModel.find_by_id(user_id)

    form = UserUpdateForm()

    if form.validate_on_submit():
        user.email=form.email.data
        user.phone = form.phone.data
        user.password_hash = generate_password_hash(form.password.data)
        user.save_to_db()

        return render_template("user_account.html", user=user)

    form.email.data = user.email
    form.phone.data = user.phone

    return render_template("user_update.html", form=form)


@user_bp.route("/close_account")
@login_required
def user_close_account():

    user_id = request.args.get("user_id")
    user= UserModel.find_by_id(user_id)
    if user:
        user.delete_from_db()

    return redirect(url_for("web.index"))

