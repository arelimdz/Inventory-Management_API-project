from init import db, ma
from marshmallow import fields


# Declare Shop model and its attributes
class Shop(db.Model):
    __tablename__ = "shops"

    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    # Register model relationships
    users = db.relationship("User", back_populates="shop")


# Create a Shop schema usign marshmallow to convert the data from the database in a Serializing Json type object
class ShopSchema(ma.Schema):
    users = fields.List(fields.Nested("UserSchema", exclude=["shop"]))

    class Meta:
        fields = ("id", "shop_name", "address", "description", "users")


# Declare Shop schema to be able to retrieve information to the frontend
# for a single shop
shop_schema = ShopSchema()
# for many shops.
shops_schema = ShopSchema(many=True)
