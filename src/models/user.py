from init import db
from .CamelCasedSchema import CamelCasedSchema
from marshmallow import fields


# Declare user model and its attributes
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    # Register Foreign Key
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"), nullable=False)

    # Register model relationships
    shop = db.relationship("Shop", back_populates="users")


# Create a marshmallow User schema
class UserSchema(CamelCasedSchema):
    shop = fields.Nested("ShopSchema", only=["shop_name", "address"])

    class Meta:
        fields = ("id", "name", "email", "password", "role", "is_admin", "shop")


# Declare user schema to be able to retrieve information to the frontend
# for a single user
user_schema = UserSchema(exclude=["password"])
# for many users.
users_schema = UserSchema(many=True, exclude=["password"])
