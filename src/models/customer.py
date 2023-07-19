from init import db, ma

# Declare customer model and its attributes
class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False )
    email = db.Column(db.String,  unique=True, nullable=False )
    address = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    authorized_discount = db.Column(db.Float, default=0)


# Create a customer schema usign marshmallow to convert the data from the database in a Serializing Json type object
class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "address", "phone_number", "authorized_discount")

# Declare customer schema to be able to retrieve information to the frontend 
# for a single customer
customer_schema = CustomerSchema()
# for many customers.
customers_schema = CustomerSchema(many=True)