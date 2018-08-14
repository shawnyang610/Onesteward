from flask import Blueprint, render_template

address_bp = Blueprint("address", __name__)

@address_bp.route("/new")
def address_new():
    return render_template("address_create.html")


@address_bp.route("/info")
def address_info():
    pass


@address_bp.route("/update")
def address_update():
    return render_template("address_create.html")



@address_bp.route("/delete")
def address_delete():
    pass