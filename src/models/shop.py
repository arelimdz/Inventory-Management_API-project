from init import db
from marshmallow import fields
from .CamelCasedSchema import CamelCasedSchema


# Declare Shop model and its attributes
class Shop(db.Model):
    __tablename__ = "shops"

    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    # Register model relationships
    users = db.relationship("User", back_populates="shop")
    stock_items = db.relationship("StockItem", back_populates="shop")


# Create a marshmallow Shop schema
class ShopSchema(CamelCasedSchema):
    users = fields.List(fields.Nested("UserSchema", exclude=["shop"]))
    stock_items = fields.List(
        fields.Nested("StockItemSchema", only=["item_name", "size", "quantity", "sku"])
    )

    class Meta:
        fields = ("id", "shop_name", "address", "description", "users")


# Declare Shop schema to be able to retrieve information to the frontend
# for a single shop
shop_schema = ShopSchema()
# for many shops.
shops_schema = ShopSchema(many=True)
