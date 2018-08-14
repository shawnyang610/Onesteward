from flask import Blueprint, render_template

post_bp = Blueprint("post", __name__)

@post_bp.route("/create")
def post_create():
    return render_template("post_create.html")


@post_bp.route("/info")
def post_info():
    return render_template("post_info.html")


@post_bp.route("/update")
def post_update():
    return render_template("post_create.html")
