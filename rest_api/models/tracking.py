from rest_api import db

# tracking logs for orders, 1 order has many logs

class TrackingModel(db.Model):
    __tablename__ = "tracking_logs"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200))

    # need inverse relation so order retrieves all its tracking logs
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    # staff who summited the tracking log
    # no need for inverse relation
    staff_id = db.Column(db.Integer, db.ForeignKey("staffs.id"))
    # user comments, coresponds to an existing staff tracking log
    # no need for inverse relation
    user_id = db.Column (db.Integer)
    is_deleted = db.Column(db.Integer)

    def __init__(self, message, order_id, staff_id, user_id):
        self.message = message
        self.order_id =order_id
        self.staff_id = staff_id
        self.user_id= user_id
        self.is_deleted=0

    def json(self):
        return {
            "id":self.id,
            "message":self.message,
            "order_id":self.order_id,
            "staff_id":self.staff_id,
            "user_id":self.user_id,
            "is_deleted":self.is_deleted
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=0).first()

    @classmethod
    def find_by_order_id(cls, order_id):
        return cls.query.filter_by(order_id=order_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_deleted=1
        db.session.add(self)
        db.session.commit()
