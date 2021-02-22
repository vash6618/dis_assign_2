from database import db_customer as db
from enum import Enum

class review_type(Enum):
    thumbs_up = 1
    thumbs_down = 2
    NA = 3

class Buyers(db.Model):
    __tablename__ = 'buyers'

    buyer_id = db.Column(db.BigInteger(), primary_key=True)
    item_id = db.Column(db.BigInteger(), primary_key=True)
    quantity = db.Column(db.Integer())
    checked_out = db.Column(db.Boolean(), primary_key=True)
    seller_review = db.Column(db.Enum(review_type), default=review_type('NA'))
