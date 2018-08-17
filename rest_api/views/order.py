from flask import Blueprint, render_template, redirect, url_for, request
from rest_api.forms.order import OrderCreateForm, OrderUpdateForm
from rest_api.models.order import OrderModel
from rest_api.models.tracking import TrackingModel

order_bp = Blueprint("order", __name__)


@order_bp.route("/create", methods=["GET","POST"])
def order_create():

    form = OrderCreateForm()

    if form.validate_on_submit():

        order = OrderModel(
            ur_code=form.ur_code.data,
            name=form.name.data,
            staff_id=form.staff_id.data
        )
        order.save_to_db()

        return redirect(url_for("order.order_info",order_id=order.id))
    
    return render_template("order_create.html", form=form)


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
def order_list():

    page = request.args.get("page", 1, type=int)
    orders = OrderModel.find_all().paginate(page=page, per_page=10)

    return render_template("order_list.html", orders=orders)