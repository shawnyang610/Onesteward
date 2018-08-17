from rest_api import db
from datetime import datetime
class RevokedTokenModel(db.Model):
    __tablename__="revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(128))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, jti):
        self.jti=jti

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        jti = cls.query.filter_by(jti=jti).first()
        return jti
