from init import db
from .CamelCasedSchema import CamelCasedSchema
from marshmallow import fields


# Declare Receipt model and its attributes
class Receipt(db.Model):
    __tablename__ = "receipts"

    # Auto-generated
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    total = db.Column(db.Numeric(10, 2), default=0)

    # Information from frontend
    payment_method = db.Column(db.String, nullable=False)
    purchase_type = db.Column(db.String, nullable=False)

    # Register Foreign Keys
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    # Register model relationships
    customer = db.relationship("Customer", back_populates="receipts")
    outgoing_stocks = db.relationship("OutgoingStock", back_populates="receipt")


# Create a Receipt schema usign marshmallow
class ReceiptSchema(CamelCasedSchema):
    customer = fields.Nested("CustomerSchema", exclude=["receipts"])
    outgoing_stocks = fields.List(
        fields.Nested("OutgoingStockSchema", exclude=["receipt"])
    )

    class Meta:
        fields = (
            "id",
            "date",
            "total",
            "payment_method",
            "purchase_type",
            "customer_id",
            "outgoing_stocks",
        )


# Declare Receipt schema to be able to retrieve information to the frontend
# for a single Receipt
receipt_schema = ReceiptSchema()
# for many Receipt.
receipts_schema = ReceiptSchema(many=True)
