from init import db
from .CamelCasedSchema import CamelCasedSchema
from marshmallow import fields


# Declare outgoing_stock model and its attributes
class OutgoingStock(db.Model):
    __tablename__ = "outgoing_stocks"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2))
    tax = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))

    # Register Foreign Key
    stock_item_id = db.Column(db.Integer, db.ForeignKey("stock_items.id"))
    receipt_id = db.Column(db.Integer, db.ForeignKey("receipts.id"))

    # Register model relationships
    stock_item = db.relationship("StockItem", back_populates="outgoing_stocks")
    receipt = db.relationship("Receipt", back_populates="outgoing_stocks")


# Create a outgoing_stock schema usign marshmallow
class OutgoingStockSchema(CamelCasedSchema):
    receipt = fields.Nested(
        "ReceiptSchema", exclude=["outgoing_stocks", "is_active"], dump_only=True
    )
    stock_item = fields.Nested(
        "StockItemSchema",
        exclude=[
            "markup_pct",
            "minimum_stock",
            "id",
            "unit_cost",
            "status",
            "special_tax",
        ],
    )
    subtotal = fields.Float()
    tax = fields.Float()
    total = fields.Float()

    class Meta:
        fields = (
            "id",
            "quantity",
            "stock_item_id",
            "stock_item",
            "receipt",
            "tax",
            "subtotal",
            "total",
        )


# Declare outgoing_stock schema to be able to retrieve information to the frontend
# for a single outgoing_stock
outgoing_stock_schema = OutgoingStockSchema()
# for many outgoing_stocks.
outgoing_stocks_schema = OutgoingStockSchema(many=True)
