from init import db
from marshmallow import fields
from datetime import date
from .CamelCasedSchema import CamelCasedSchema
from sqlalchemy import UniqueConstraint


# Declare incoming_stock model and its attributes
class IncomingStock(db.Model):
    __tablename__ = "incoming_stocks"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today())
    quantity = db.Column(db.Integer, nullable=False)
    item_cost = db.Column(db.Numeric(10, 2), nullable=False)
    invoice_number = db.Column(db.String, nullable=False)

    # Foreign Keys
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    stock_item_id = db.Column(
        db.Integer, db.ForeignKey("stock_items.id"), nullable=False
    )

    # Register model relationships
    supplier = db.relationship("Supplier", back_populates="incoming_stocks")
    stock_item = db.relationship("StockItem", back_populates="incoming_stocks")

    # Create a unique constraint on stock_item_id and invoice_number
    __table_args__ = (UniqueConstraint("stock_item_id", "invoice_number"),)


# Create a incoming_stock schema usign marshmallow
class IncomingStockSchema(CamelCasedSchema):
    item_cost = fields.Float()
    supplier = fields.Nested("SupplierSchema", only=["name", "id", "email"])
    stock_item = fields.Nested(
        "StockItemSchema",
        only=[
            "id",
            "item_name",
            "item_brand",
            "size",
            "sku",
            "unit_cost",
            "quantity",
        ],
    )

    class Meta:
        fields = (
            "id",
            "date",
            "quantity",
            "item_cost",
            "invoice_number",
            "supplier",
            "stock_item",
        )


# Declare incoming_stock schema to be able to retrieve information to the frontend
# for a single incoming_stock
incoming_stock_schema = IncomingStockSchema()
# for many incoming_stocks.
incoming_stocks_schema = IncomingStockSchema(many=True)
