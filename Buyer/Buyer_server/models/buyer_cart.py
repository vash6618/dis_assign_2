from database import db_customer as db
from enum import Enum

class review_type(Enum):
    UP = 1
    DOWN = 2
    NA = 3

class BuyerCart(db.Model):
    __tablename__ = 'buyer_cart'

    buyer_id = db.Column(db.BigInteger(), primary_key=True)
    item_id = db.Column(db.BigInteger(), primary_key=True)
    quantity = db.Column(db.Integer())
    checked_out = db.Column(db.Boolean(), primary_key=True, default=False)
    seller_review = db.Column(db.Enum(review_type))
    updated_at = db.Column(db.DateTime(), primary_key=True)