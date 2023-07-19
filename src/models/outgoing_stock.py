from init import db, ma
from marshmallow import fields


# Declare outgoing_stock model and its attributes
class Outgoing_stock(db.Model):
    __tablename__ = "outgoing_stocks"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    # Register Foreign Key
    stock_item_id = db.Column(
        db.Integer, db.ForeignKey("stock_items.id", nullable=False)
    )
    receipt_id = db.Column(db.Integer, db.ForeignKey("receipts.id", nullable=False))

    # Register model relationships
    stock_item = db.relationship("Stock_item", back_populates="outgoing_stocks")
    receipt = db.relationship("Receipts", back_populates="outgoing_stocks")


# Create a outgoing_stock schema usign marshmallow to convert the data from the database in a Serializing Json type object
class Outgoing_stockSchema(ma.Schema):
    stock_item = fields.Nested(
        "Stock_itemSchema",
        exclude=[
            "quantity",
            "profit_percentage",
            "minimum_stock",
            "incoming_stock",
            "outgoing_stock",
        ],
    )
    receipt = fields.Nested("ReceiptSchema", exclude=["outgoing_stock"])

    class Meta:
        fields = ("id", "quantity", "stock_item", "receipt")


# Declare outgoing_stock schema to be able to retrieve information to the frontend
# for a single outgoing_stock
outgoing_stock_schema = Outgoing_stockSchema()
# for many outgoing_stocks.
outgoing_stocks_schema = Outgoing_stockSchema(many=True)
