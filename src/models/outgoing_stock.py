from init import db, ma

# Declare outgoing_stock model and its attributes
class Outgoing_stock(db.Model):
    __tablename__ = "outgoing_stocks"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)


    
# Create a outgoing_stock schema usign marshmallow to convert the data from the database in a Serializing Json type object
class Outgoing_stockSchema(ma.Schema):
    class Meta:
        fields = ("id", "quantity")

# Declare outgoing_stock schema to be able to retrieve information to the frontend 
# for a single outgoing_stock
outgoing_stock_schema = Outgoing_stockSchema()
# for many outgoing_stocks.
outgoing_stocks_schema = Outgoing_stockSchema(many=True)