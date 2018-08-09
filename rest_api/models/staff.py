from rest_api import db


class StaffModel(db.Model):
    __tablename__ = "staffs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password_hash = db.Column (db.String(256))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    company = db.relationship("CompanyModel")
    is_deleted = db.Column(db.Integer)

    def __init__(self, name, password_hash,company_id):
        self.name =name
        self.password_hash = password_hash
        self.company_id=company_id
        self.is_deleted = 0

    def json(self):
        if not self.company:
            ret_msg = {
                "id": self.id,
                "name": self.name,
                "is_deleted":self.is_deleted
            }
        else:
            ret_msg = {
                "id": self.id,
                "name": self.name,
                "company": self.company.json(),
                "is_deleted":self.is_deleted
             }
        return ret_msg,200



    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, is_deleted=0).first()

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
