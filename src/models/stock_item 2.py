from init import db, ma

# Declare Stock_items model and its attributes
class Stock_item(db.Model):
    __tablename__ = "stock_items"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    item_name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    sales_price = db.Column(db.Float, nullable=False)
    profit_percentage = db.Column(db.Float())


    
# Create a stock_item schema usign marshmallow to convert the data from the database in a Serializing Json type object
class stock_itemSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "role", "is_admin")

# Declare stock_item schema to be able to retrieve information to the frontend 
# for a single stock_item
stock_item_schema = stock_itemSchema(exclude = ['password'])
# for many stock_items.
stock_items_schema = stock_itemSchema(many=True, exclude = ["password"])