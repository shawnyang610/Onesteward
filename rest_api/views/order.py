from flask import Blueprint, render_template

order_bp = Blueprint("order", __name__)

@order_bp.route("/new")
def order_new():
    return render_template("order_info.html")


@order_bp.route("/info")
def order_info():
    return render_template("order_info.html")


@order_bp.route("/update")
def order_update():
    return render_template("order_info.html")



@order_bp.route("/delete")
def order_delete():
    return render_template("order_info.html")
