from rest_api import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    hashed_password = db.Column(db.String(256))
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))

    orders = db.relationship("OrderModel", lazy="dynamic")
    is_deleted = db.Column(db.Integer(1))

    def __init__(self, hashed_password, name, email):
        self.hashed_password=hashed_password
        self.name = name
        self. email = email
        self. phone = None
        self.is_deleted = 0

    def json(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "phone":self.phone,
            "orders": [order.json() for order in self.orders.all()],
            "is_deleted":self.is_deleted
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

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
