from init import db
from .CamelCasedSchema import CamelCasedSchema
from marshmallow import fields


# Declare customer model and its attributes
class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    authorised_discount = db.Column(db.Numeric(5, 2), default=0)

    # Register model relationships
    receipts = db.relationship("Receipt", back_populates="customer")


# Create a customer schema usign marshmallow
class CustomerSchema(CamelCasedSchema):
    receipts = fields.List(fields.Nested("ReceiptSchema", exclude=["customer"]))
    authorised_discount = fields.Float()

    class Meta:
        fields = (
            "id",
            "name",
            "email",
            "address",
            "city",
            "phone_number",
            "authorised_discount",
            "receipts",
        )


# Declare customer schema to be able to retrieve information to the frontend
# for a single customer
customer_schema = CustomerSchema()
# for many customers.
customers_schema = CustomerSchema(many=True)
