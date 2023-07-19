from init import db, ma

# Declare incoming_stock model and its attributes
class Incoming_stock(db.Model):
    __tablename__ = "incoming_stocks"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    quantity = db.Column(db.Integer, nullable=False)
    item_cost = db.Column(db.Float, nullable=False)
    invoice_number = db.Column(db.Integer(), nullable=False)


# Create a incoming_stock schema usign marshmallow to convert the data from the database in a Serializing Json type object
class Incoming_stockSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "quantity", "item_cost", "invoice_number")

# Declare incoming_stock schema to be able to retrieve information to the frontend 
# for a single incoming_stock
incoming_stock_schema = Incoming_stockSchema()
# for many incoming_stocks.
incoming_stocks_schema = Incoming_stockSchema(many=True)