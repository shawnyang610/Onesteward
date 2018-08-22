from rest_api import db
from rest_api.models.address import AddressModel # noqa
from datetime import datetime

class CompanyModel(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    is_deleted =db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    staffs = db.relationship("StaffModel", back_populates="company")

    addresses = db.relationship ("AddressModel", lazy="dynamic")

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.is_deleted=0

    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "phone":self.phone,
            "is_deleted": self.is_deleted,
            "addresses": [address.json() for address in self.addresses.all()]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=0).first()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name, is_deleted=0).first()


    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email, is_deleted=0).first()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(is_deleted=0).order_by(CompanyModel.name)


    def get_active_addresses(self):

        addresses = self.addresses.all()

        active_addresses = filter(lambda address: address.is_deleted==0, addresses)

        return active_addresses


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()

