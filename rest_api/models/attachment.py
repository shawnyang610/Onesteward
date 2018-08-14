from rest_api import db
from datetime import datetime

# attachment for tracking logs / user posts, many to one

class AttachmentModel(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)
    attachment_name = db.Column(db.String(200), nullable=False, unique=True)

    # need inverse relation so order retrieves all its tracking logs
    track_log_id = db.Column(db.Integer, db.ForeignKey("tracking_logs.id"))

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    is_deleted =db.Column(db.Integer, default=0)


    def __init__(self, attachment_name, track_log_id):
        self.attachment_name = attachment_name
        self.track_log_id = track_log_id

    def json(self):
        return {
            "id":self.id,
            "attachment_name":self.attachment_name,
            "track_log_id": self.track_log_id
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=0).first()

    @classmethod
    def find_by_track_log_id(cls, track_log_id):
        return cls.query.filter_by(track_log_id=track_log_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()