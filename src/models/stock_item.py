from init import db, ma
from marshmallow import fields


# Declare Stock_items model and its attributes
class Stock_item(db.Model):
    __tablename__ = "stock_items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    item_description = db.Column(db.String(100), nullable=False)
    item_brand = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, nullable=False)
    markup_pct = db.Column(db.Float)
    minimum_stock = db.Column(db.Integer)
    sku = db.Column(db.String, nullable=False)  # Supplier SKU
    special_tax = db.Column(
        db.Float, default=10
    )  # Some products migth have special tax
    status = db.column(db.String, default="Active")

    # # Register Foreign Key
    # shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)

    # # Register model relationships
    # incoming_stocks = db.relationship("Incoming_stock", back_populates="stock_item")
    # shop = db.relationship("Shop", back_populates="stock_items")
    # outgoing_stocks = db.relationship("Outgoing_stock", back_populates="stock_item")


# Create a stock_item schema usign marshmallow to convert the data from the database in a Serializing Json type object
class Stock_itemSchema(ma.Schema):
    # incoming_stocks = fields.List(
    #     fields.Nested("Incoming_stockSchema", exclude=["stock_item"])
    # )
    # shop = fields.Nested("ShopSchema", only=["name", "address"])
    # outgoing_stocks = fields.List(
    #     fields.Nested("Outgoing_stockSchema", exclude=["stock_item"])
    # )

    class Meta:
        fields = (
            "id",
            "item_name",
            "item_description",
            "item_brand",
            "size",
            "sku",
            "category",
            "quantity",
            "unit_price",
            "markup_pct",
            "minimum_stock",
            "special_tax",
            "status",
            # "shop",
            # "incoming_stocks",
            # "outgoing_stocks"
        )
        ordered = True


# Declare stock_item schema to be able to retrieve information to the frontend
# for a single stock_item
stock_item_schema = Stock_itemSchema()
# for many stock_items.
stock_items_schema = Stock_itemSchema(many=True)
