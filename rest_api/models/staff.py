from rest_api import db
from rest_api.models.company import CompanyModel # noqa
# from rest_api.models.order import OrderModel # noqa
from datetime import datetime
from flask_login import UserMixin
class StaffModel(db.Model, UserMixin):
    __tablename__ = "staffs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    role = db.Column(db.String(15))
    password_hash = db.Column (db.String(256))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    company = db.relationship("CompanyModel", back_populates="staffs", uselist=False)
    orders = db.relationship("OrderModel", back_populates="staff")
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    is_deleted = db.Column(db.Integer)

    def __init__(self, name, role,password_hash,company_id):
        self.name =name
        self.role = role
        self.password_hash = password_hash
        self.company_id=company_id
        self.is_deleted = 0

    def json(self):
        if not self.company:
            ret_msg = {
                "id": self.id,
                "name": self.name,
                "role": self.role,
                "is_deleted":self.is_deleted
            }
        else:
            ret_msg = {
                "id": self.id,
                "name": self.name,
                "role": self.role,
                "company": self.company.json(),
                "is_deleted":self.is_deleted
             }
        return ret_msg,200

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=0).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, is_deleted=0).first()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(is_deleted=0).order_by(cls.company_id)
    @classmethod
    def find_by_company_id(cls, company_id):
        return cls.query.filter_by(company_id=company_id, is_deleted=0).order_by(cls.name)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()


    ############################
    #### overrides UserMixin. adding "staff_" identifier to distinguish
    #### from users during @flask_login.user_loader callback. ###########
    def get_id(self):
        try:
            return "staff_"+str(self.id)

        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')