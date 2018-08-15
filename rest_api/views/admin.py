from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/control_panel")
def control_panel():
    return render_template("admin_control_panel.html")
