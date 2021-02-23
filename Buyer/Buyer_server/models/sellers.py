from database import db_customer as db
from enum import Enum


class seller_feedback(Enum):
    up = "thumbs_up"
    down = "thumbs_down"

class Sellers(db.Model):
    __tablename__ = 'sellers'

    name = db.Column(db.String())
    id = db.Column(db.BigInteger(), primary_key=True)
    feedback = db.Column(db.ARRAY(db.Integer()))
    num_items_sold = db.Column(db.Integer())
    user_name = db.Column(db.String())
    password = db.Column(db.String())
    db.UniqueConstraint('user_name', name='user_name_seller_index')




