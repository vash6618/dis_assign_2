from database import db_customer as db

class Buyers(db.Model):
    __tablename__ = 'buyers'

    name = db.Column(db.String())
    id = db.Column(db.BigInteger(), primary_key=True)
    num_items_purchased = db.Column(db.Integer())
    user_name = db.Column(db.String())
    password = db.Column(db.String())
