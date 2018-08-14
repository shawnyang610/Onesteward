from flask import Blueprint, render_template

trk_log_bp = Blueprint("tracking_log", __name__)

@trk_log_bp.route("/new")
def tracking_log_new():
    return render_template("tracking_log.html")


@trk_log_bp.route("/info")
def tracking_log_info():
    return render_template("tracking_log.html")


@trk_log_bp.route("/update")
def tracking_log_update():
    return render_template("tracking_log.html")


@trk_log_bp.route("/delete")
def tracking_log_delete():
    return render_template("tracking_log.html")