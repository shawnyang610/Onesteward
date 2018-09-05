from flask import Blueprint, render_template, redirect, url_for, request
from rest_api.forms.order import OrderCreateForm, OrderUpdateForm, OrderCheckStatusByNumberForm, OrderCheckStatusByQRCodeForm
from rest_api.models.order import OrderModel
from rest_api.models.tracking import TrackingModel
from rest_api.models.company import CompanyModel
from flask_login import login_required, current_user
from rest_api.models.staff import StaffModel
from rest_api.controls.auth import (
    is_admin,
    is_company_admin,
    is_staff,
    is_user,
    render_error_page_unauthorized_access)
from rest_api.controls.urcode_generator import (
    generate_qrcode,
    generate_order_number,
    generate_and_validate_order_number,
    decode_qrcode)

order_bp = Blueprint("order", __name__)


@order_bp.route("/create", methods=["GET","POST"])
@login_required
def order_create():

    if is_user(current_user):
        return render_error_page_unauthorized_access()

    form = OrderCreateForm()

    if form.validate_on_submit():

        order = OrderModel(
            ur_code=form.ur_code.data,
            name=form.name.data,
            staff_id=form.staff_id.data
        )
        order.save_to_db()

        return redirect(url_for("order.order_info",order_id=order.id))
    
    order_number = generate_and_validate_order_number(generate_order_number)
    generate_qrcode(order_number)
    form.ur_code.data = order_number
    form.staff_id.data=current_user.id
    extension=".jpg"
    return render_template("order_create.html", form=form, extension=extension)


@order_bp.route("/update/<int:order_id>", methods=["GET","POST"])
def order_update(order_id):

    order = OrderModel.find_by_id(order_id)

    form = OrderUpdateForm()

    if form.validate_on_submit():
        order.name = form.name.data
        order.staff_id = form.staff_id.data
        order.save_to_db()
        return redirect(url_for("order.order_info", order_id=order.id))

    form.name.data = order.name
    form.staff_id.data = order.staff_id
    return render_template("order_update.html", form=form)


@order_bp.route("/info/<int:order_id>", methods=["GET","POST"])
def order_info(order_id):

    order = OrderModel.find_by_id(order_id)

    page = request.args.get("page", 1, type=int)

    posts = TrackingModel.find_by_order_id(order_id).paginate(page=page, per_page=10)

    return render_template("order_info.html", order=order, posts=posts)


@order_bp.route("/delete/<int:order_id>")
def order_delete(order_id):
    order = OrderModel.find_by_id(order_id)

    if order:
        order.delete_from_db()

        return redirect(url_for("order.order_list"))


@order_bp.route("/list")
@login_required
def order_list():
    
    page = request.args.get("page", 1, type=int)

    if is_admin(current_user):
        orders = OrderModel.find_all().paginate(page=page, per_page=5)

    elif is_company_admin(current_user):
        orders=OrderModel.find_by_company(current_user.company).paginate(page=page, per_page=5)
        # orders=OrderModel.find_by_company_id(current_user.company_id).paginate(page=page, per_page=5)

    elif is_staff(current_user):
        orders = OrderModel.find_by_staff_id(current_user.id).paginate(page=page, per_page=5)
    elif is_user(current_user):
        orders = OrderModel.find_by_user_id(current_user.id).paginate(page=page, per_page=5)

    return render_template("order_list.html", orders=orders)



@order_bp.route("check_status", methods=["GET","POST"])
def order_check_status():
    form = OrderCheckStatusByNumberForm()

    if form.validate_on_submit():
        order = OrderModel.find_by_ur_code(form.order_number.data)
        if order:
            return redirect(url_for("order.order_info", order_id=order.id))

    return render_template("order_check_status.html", form=form)

@order_bp.route("check_status_qrcode", methods=["GET","POST"])
def order_check_status_qrcode():
    form = OrderCheckStatusByQRCodeForm()

    if form.validate_on_submit():

        decoded_data = decode_qrcode(form.qrcode_img.data)

        order = OrderModel.find_by_ur_code(decoded_data)
        if order:
            return redirect(url_for("order.order_info", order_id=order.id))

    return render_template("order_check_status.html", form=form)