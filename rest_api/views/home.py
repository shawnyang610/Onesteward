from flask import Blueprint, render_template

home_bp = Blueprint("web", __name__)

@home_bp.route("/")
def index():
    return render_template("home.html")