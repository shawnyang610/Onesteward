from rest_api import db
from rest_api.models.tracking import TrackingModel # noqa
# from rest_api.models.staff import StaffModel
# from rest_api.models.company import CompanyModel




class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    ur_code = db.Column (db.String(100))
    # name of the ordered service
    name = db.Column(db.String(80))
    staff_id = db.Column(db.Integer, db.ForeignKey("staffs.id"))
    # filled in when user registers new account and add this order in account
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    is_deleted = db.Column(db.Integer)

    tracking_logs = db.relationship("TrackingModel", lazy="dynamic")

    def __init__(self, ur_code, name, staff_id):
        self.ur_code = ur_code
        self.name = name
        self.staff_id = staff_id
        # user_id = 1 is unregistered user, updates when user registers account
        self.user_id = 1
        self.is_deleted=0

    def json(self):
        return {
            "id":self.id,
            "ur_code":self.ur_code,
            "name":self.name,
            "staff_id":self.staff_id,
            "user_id":self.user_id,
            "tracking_logs": [log.jason() for log in self.tracking_logs.all()],
            "is_deleted":self.is_deleted
        }

    @classmethod
    def find_by_ur_code(cls,ur_code):
        return cls.query.filter_by(ur_code=ur_code, is_deleted=0).first()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(is_deleted=0)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()
