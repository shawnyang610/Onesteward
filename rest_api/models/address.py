from rest_api import db

# company addresses, each company can have many locations
class AddressModel(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    is_deleted = db.Column(db.Integer)
    line1 = db.Column (db.String(80))
    line2 = db.Column (db.String(80))
    city = db.Column (db.String(80))
    state = db.Column (db.String(80))
    zip = db.Column (db.String(10))

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    company = db.relationship("CompanyModel")


    def __init__(self, line1, line2, city, state, zip, company_id):
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.state = state
        self.zip = zip
        self.company_id=company_id
        self.is_deleted = 0

    def json(self):
        return{
            "id": self.id,
            "line1": self.line1,
            "line2": self.line2,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "company_id":self.company_id,
            "is_deleted":self.is_deleted
        }

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id = id).first()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(is_deleted=0)

    def save_to_db (self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db (self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()
