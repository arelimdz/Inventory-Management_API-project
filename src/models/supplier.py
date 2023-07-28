from init import db
from marshmallow import fields
from .CamelCasedSchema import CamelCasedSchema


# Declare Supplier model and its attributes
class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    address = db.Column(db.String)

    # Register model relationships
    incoming_stock = db.relationship("IncomingStock", back_populates="supplier")


# Create a Supplier schema usign marshmallow
class SupplierSchema(CamelCasedSchema):
    incoming_stocks = fields.List(
        fields.Nested("IncomingStockSchema", exclude=["supplier"])
    )

    class Meta:
        fields = ("id", "name", "email", "phone_number", "address", "incoming_stock")


# Declare Supplier schema to be able to retrieve information to the frontend
# for a single Supplier
supplier_schema = SupplierSchema()
# for many Suppliers.
suppliers_schema = SupplierSchema(many=True)
