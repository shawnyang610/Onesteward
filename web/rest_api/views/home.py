from flask import Blueprint, render_template, redirect, url_for,request
from rest_api.forms.order import OrderCheckStatusByNumberForm, OrderCheckStatusByQRCodeForm
from rest_api.models.order import OrderModel
from rest_api.controls.urcode_generator import decode_qrcode
home_bp = Blueprint("web", __name__)

@home_bp.route("/", methods=["GET","POST"])
def index():
    search_method = request.args.get("search_method", "by_order_number", type=str)

    if search_method == "by_order_number":
        form = OrderCheckStatusByNumberForm()
        if form.validate_on_submit():
            order = OrderModel.find_by_ur_code(form.order_number.data)
            if order:
                return redirect(url_for("order.order_info", order_id=order.id)) 

    else:
        form = OrderCheckStatusByQRCodeForm()
        if form.validate_on_submit():
            decoded_data = decode_qrcode(form.qrcode_img.data)
            order = OrderModel.find_by_ur_code(decoded_data)
            if order:
                return redirect(url_for("order.order_info", order_id=order.id))

    return render_template("home.html", form=form, search_method=search_method)
