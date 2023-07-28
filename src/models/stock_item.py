from init import db
from marshmallow import fields
from .CamelCasedSchema import CamelCasedSchema


# Declare StockItem model and its attributes
class StockItem(db.Model):
    __tablename__ = "stock_items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    item_description = db.Column(db.String(100), nullable=False)
    item_brand = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit_cost = db.Column(db.Numeric(100, 2), nullable=False)
    unit_price = db.Column(db.Numeric(100, 2), nullable=False)
    markup_pct = db.Column(db.Numeric(5, 2), nullable=False)
    minimum_stock = db.Column(db.Integer, nullable=False)
    sku = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )  # Supplier SKU
    special_tax = db.Column(
        db.Numeric(5, 2), default=10
    )  # Some products migth have special tax
    status = db.Column(db.String, default="Active")

    # Register Foreign Key
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)

    # # Register model relationships
    incoming_stocks = db.relationship("IncomingStock", back_populates="stock_item")
    shop = db.relationship("Shop", back_populates="stock_items")
    outgoing_stocks = db.relationship("OutgoingStock", back_populates="stock_item")


# Create a stock_item schema usign marshmallow
class StockItemSchema(CamelCasedSchema):
    incoming_stocks = fields.List(
        fields.Nested("IncomingStockSchema", exclude=["stock_item"])
    )
    shop = fields.Nested("ShopSchema", only=["shop_name", "address"])
    outgoing_stocks = fields.List(
        fields.Nested("OutgoingStockSchema", exclude=["stock_item"])
    )

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
            "unit_cost",
            "unit_price",
            "markup_pct",
            "minimum_stock",
            "special_tax",
            "status",
            "shop_id",
            "incoming_stocks",
            "outgoing_stock",
        )


# Declare stock_item schema to be able to retrieve information to the frontend
# for a single stock_item
stock_item_schema = StockItemSchema()
# for many stock_items.
stock_items_schema = StockItemSchema(many=True)
