"""Module that manages database connection."""
import os
from gino import Gino, create_engine
from config import DBConstants

# pylint: disable=invalid-name
# Connect to the database
db_product = None
db_customer = None
async def connect_db():
    import ssl

    ctx = ssl.create_default_context(cafile="")
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    global db_product, db_customer
    db_product = Gino()
    db_customer = Gino()
    await db_product.set_bind(DBConstants.DB_product, echo=True, ssl=ctx)
    await db_customer.set_bind(DBConstants.DB_customer, echo=True, ssl=ctx)
    print(db_product)
    print("db_customer:", end=" ")
    print(db_customer)