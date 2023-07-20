from init import db, ma
from .CamelCasedSchema import CamelCasedSchema


# Declare user model and its attributes
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    is_admin = db.Column(db.Boolean, default=False)


# Create a user schema usign marshmallow to convert the data from the database in a Serializing Json type object
class UserSchema(CamelCasedSchema):
    class Meta:
        fields = ("id", "name", "email", "password", "role", "is_admin")


# Declare user schema to be able to retrieve information to the frontend
# for a single user
user_schema = UserSchema(exclude=["password"])
# for many users.
users_schema = UserSchema(many=True, exclude=["password"])
