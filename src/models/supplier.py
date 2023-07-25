from init import db
from .CamelCasedSchema import CamelCasedSchema


# Declare Supplier model and its attributes
class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    address = db.Column(db.String)


# Create a Supplier schema usign marshmallow
class SupplierSchema(CamelCasedSchema):
    class Meta:
        fields = ("id", "name", "email", "phone_number", "address")


# Declare Supplier schema to be able to retrieve information to the frontend
# for a single Supplier
supplier_schema = SupplierSchema()
# for many Suppliers.
suppliers_schema = SupplierSchema(many=True)
