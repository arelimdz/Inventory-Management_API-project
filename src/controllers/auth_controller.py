from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def auth_registrer():
    try:
        # Access to the information from the frontend (user info) and stored it in the variable body_data
        body_data = request.get_json()

        # Create a new User model instance from user info (in body_data)
        user = User()  # Instance of the User class
        user.name = body_data.get("name")
        user.email = body_data.get("email")
        user.role = body_data.get("role")
        if body_data.get("password"):
            user.password = bcrypt.generate_password_hash(
                body_data.get("password")
            ).decode("utf-8")

        # Add the user to the session
        db.session.add(user)
        # Commit to add the user to the database
        db.session.commit()
        # Respond to the client (pass to the front-end)
        return user_schema.dump(user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "The email address is already in use"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}, 409
