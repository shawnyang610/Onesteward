from flask import Blueprint, render_template
from flask_login import current_user, login_required
from rest_api.controls.auth import is_admin, render_error_page_unauthorized_access


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/control_panel")
@login_required
def control_panel():

    if not is_admin(current_user):
        return render_error_page_unauthorized_access()
    
    return render_template("admin_control_panel.html")