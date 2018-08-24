from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField # noqa
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed
import os
from flask import current_app


class PostCreateForm(FlaskForm):

    message = StringField("Message", validators=[DataRequired()])
    # order_id = IntegerField("Order ID", validators=[DataRequired(), NumberRange()])
    staff_id = IntegerField("Staff ID", validators=[DataRequired(), NumberRange()])
    user_id = IntegerField("User ID", validators=[DataRequired(), NumberRange()])
    attachment = FileField("Add Attachment", validators=[FileAllowed(["jpg","pdf","png"])])
    submit = SubmitField("Post")

class PostUpdateForm(FlaskForm):
    pass


def save_attachment(file_upload, post_id):
    
    filename = file_upload.filename
    filename_without_ext = filename.split(".")[0]
    ext_type=filename.split(".")[-1]
    storage_filename = filename_without_ext+ "_"+str(post_id)+"."+ext_type

    filepath = os.path.join(current_app.root_path, "static", storage_filename)

    file_upload.save(filepath)
    
    return storage_filename
