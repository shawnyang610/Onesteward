from flask import Blueprint, render_template, redirect, url_for
from rest_api.models.tracking import TrackingModel
from rest_api.models.order import OrderModel
from rest_api.forms.post import PostCreateForm, save_attachment
from rest_api.models.attachment import AttachmentModel
from flask_login import login_required, current_user
from rest_api.controls.auth import is_user
post_bp = Blueprint("post", __name__)

@post_bp.route("/create/<int:order_id>", methods=["GET","POST"])
@login_required
def post_create(order_id):

    order = OrderModel.find_by_id(order_id)
    form = PostCreateForm()

    if form.validate_on_submit():
        post = TrackingModel(
            message=form.message.data,
            order_id=order_id,
            staff_id=form.staff_id.data,
            user_id=form.user_id.data
        )
        post.save_to_db()

        if form.attachment.data:

            storage_filename = save_attachment(form.attachment.data, post.id)

            attachment = AttachmentModel(
                attachment_name=storage_filename,
                track_log_id=post.id
            )
            attachment.save_to_db()

        return redirect(url_for("order.order_info", order_id=order_id))

    if is_user(current_user):
        form.staff_id.data=order.staff_id
        form.user_id.data=current_user.id
    else:
        form.user_id.data=order.user_id
        form.staff_id.data=current_user.id
    return render_template("post_create.html", form=form)





@post_bp.route("/info")
def post_info():
    return render_template("post_info.html")


@post_bp.route("/update")
def post_update():
    return render_template("post_create.html")
