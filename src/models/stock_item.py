from init import db, ma
from marshmallow import fields


# Declare Stock_items model and its attributes
class Stock_item(db.Model):
    __tablename__ = "stock_items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    item_description = db.Column(db.String)
    size = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    sales_price = db.Column(db.Float, nullable=False)
    profit_percentage = db.Column(db.Float)
    minimum_stock = db.Column(db.Integer)
    sku = db.Column(db.String, nullable=False)  # Supplier SKU

    # Register Foreign Key
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)

    # Register model relationships
    incoming_stocks = db.relationship("Incoming_stock", back_populates="stock_item")
    shop = db.relationship("Shop", back_populates="stock_items")
    outgoing_stocks = db.relationship("Outgoing_stock", back_populates="stock_item")


# Create a stock_item schema usign marshmallow to convert the data from the database in a Serializing Json type object
class Stock_itemSchema(ma.Schema):
    incoming_stocks = fields.List(
        fields.Nested("Incoming_stockSchema", exclude=["stock_item"])
    )
    shop = fields.Nested("ShopSchema", only=["name", "address"])
    outgoing_stocks = fields.List(
        fields.Nested("Outgoing_stockSchema", exclude=["stock_item"])
    )

    class Meta:
        fields = (
            "id",
            "item_name",
            "item_description",
            "size",
            "category",
            "quantity",
            "sales_price",
            "profit_percentage",
            "minimum_stock",
            "shop",
            "incoming_stocks",
            "outgoing_stocks"
        )


# Declare stock_item schema to be able to retrieve information to the frontend
# for a single stock_item
stock_item_schema = Stock_itemSchema()
# for many stock_items.
stock_items_schema = Stock_itemSchema(many=True)
