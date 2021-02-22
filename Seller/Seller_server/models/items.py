from database import db_product as db


class Items(db.Model):
    __tablename__ = 'items'

    name = db.Column(db.String())
    category = db.Column(db.SmallInteger())
    id = db.Column(db.BigInteger(), primary_key=True)
    condition = db.Column(db.Boolean())
    keywords = db.Column(db.ARRAY(db.String()))
    sale_price = db.Column(db.Float())
    quantity = db.Column(db.Integer())
    seller_id = db.Column(db.BigInteger())
