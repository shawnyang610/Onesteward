from rest_api import db


class CompanyModel(db.Model):

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    is_deleted =db.Column(db.Integer)

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
            "addresses": [address.jason() for address in self.addresses.all()]
        }

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

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
