from init import db, ma
from marshmallow import fields


# Declare incoming_stock model and its attributes
class Incoming_stock(db.Model):
    __tablename__ = "incoming_stocks"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    quantity = db.Column(db.Integer, nullable=False)
    item_cost = db.Column(db.Float, nullable=False)
    invoice_number = db.Column(db.Integer, nullable=False)

    # Foreign Keys
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    stock_item_id = db.Column(
        db.Integer, db.ForeignKey("stock_items.id"), nullable=False
    )

    # Register model relationships
    supplier = db.relationship("Supplier", back_populates="incoming_stocks")
    stock_item = db.relationship(
        "Stock_item", back_populates="incoming_stocks", cascade="all, delete"
    )


# Create a incoming_stock schema usign marshmallow to convert the data from the database in a Serializing Json type object
class Incoming_stockSchema(ma.Schema):
    supplier = fields.Nested("SupplierSchema", only=["name"])
    stock_item = field.Nested(
        "Stock_itemSchema", exclude=["incoming_stocks"]
    )  # <----CHECK LATER

    class Meta:
        fields = (
            "id",
            "date",
            "quantity",
            "item_cost",
            "invoice_number",
            "supplier",
            "stock_items",
        )


# Declare incoming_stock schema to be able to retrieve information to the frontend
# for a single incoming_stock
incoming_stock_schema = Incoming_stockSchema()
# for many incoming_stocks.
incoming_stocks_schema = Incoming_stockSchema(many=True)
