from rest_api import db


class StaffModel(db.Model):
    __tablename__ = "staffs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    is_deleted = db.Column(db.Integer(1))

    def __init__(self, name, company_id):
        self.name =name
        self.company_id=company_id
        self.is_deleted = 0

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "company_id":self.company_id,
            "is_deleted":self.is_deleted
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()
