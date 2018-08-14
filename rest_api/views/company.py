from flask import Blueprint

company_bp = Blueprint("company", __name__)

@company_bp.route("/new")
def company_new():
    return "<h1> i'm from company</h1>"


@company_bp.route("/info")
def company_info():
    pass


@company_bp.route("/update")
def company_update():
    pass


@company_bp.route("/close_account")
def company_close_account():
    pass