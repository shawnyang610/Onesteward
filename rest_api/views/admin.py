from flask import Blueprint, render_template
from flask_login import login_user, current_user, logout_user, login_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/control_panel")
@login_required
def control_panel():
    return render_template("admin_control_panel.html")
