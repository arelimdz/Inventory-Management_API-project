from init import db, ma

# Declare Receipt model and its attributes
class Receipt(db.Model):
    __tablename__ = "receipts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    total =db.Column(db.Float)
    payment_method = db.Column(db.String, nullable=False)
    purchase_type = db.Column(db.String, nullable=False)


    
# Create a Receipt schema usign marshmallow to convert the data from the database in a Serializing Json type object
class ReceiptSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "total", "payment_method", "purchase_type")

# Declare Receipt schema to be able to retrieve information to the frontend 
# for a single Receipt
receipt_schema = ReceiptSchema()
# for many Receipt.
receipts_schema = ReceiptSchema(many=True)