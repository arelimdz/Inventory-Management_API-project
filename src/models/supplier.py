from init import db, ma
from marshmallow import fields


# Declare Supplier model and its attributes
class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    address = db.Column(db.String)

    # Register model relationships
    incoming_stock = db.relationship("Incoming_stock", back_populates="incoming_stock")


# Create a Supplier schema usign marshmallow to convert the data from the database in a Serializing Json type object
class SupplierSchema(ma.Schema):
    incoming_stocks = fields.List(
        fields.Nested("Incoming_stockSchema", exclude=["supplier"])
    )

    class Meta:
        fields = ("id", "name", "email", "phone_number", "address", "incoming_stocks")


# Declare Supplier schema to be able to retrieve (dump) information to the frontend
# for a single Supplier
supplier_schema = SupplierSchema()
# for many Suppliers.
suppliers_schema = SupplierSchema(many=True)
