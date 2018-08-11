from rest_api import db

class RevokedTokenModel(db.Model):
    __tablename__="revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(128))

    def __init__(self, jti):
        self.jti=jti

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        jti = cls.query.filter_by(jti=jti).first()
        return jti
