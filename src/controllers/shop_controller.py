from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorise_as_admin
from models.shop import Shop, shop_schema, shops_schema
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

shops_blueprint = Blueprint("shop", __name__, url_prefix="/shops")


# Return information af all shop including all shop users
@shops_blueprint.route("/", methods=["GET"])
def get_all_shops():
    stmt = db.select(Shop)
    shops = db.session.scalars(stmt)
    return shops_schema.dump(shops)


# Return information of a single shop
@shops_blueprint.route("/<int:id>", methods=["GET"])
def get_one_shop(id):
    stmt = db.select(Shop).filter_by(id=id)
    shop = db.session.scalar(stmt)
    if shop:
        return shop_schema.dump(shop)
    else:
        return {"error": f"Shop with id {id} not found"}


@shops_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_new_shop():
    # Check if user has authorisation to performe action
    is_admin = authorise_as_admin()
    if not is_admin:
        return {"error": "Only Shop Manager can add new shop"}, 403
    # Access to the information from the frontend and
    # stored it in the variable body_data
    try:
        body_data = shop_schema.load(request.get_json())
        
        # Create a new Shop model instance
        shop = Shop(
            shop_name=body_data.get("shop_name"),
            address=body_data.get("address"),
            description=body_data.get("description"),
        )
        # Add that Shop to the session
        db.session.add(shop)
        # Commit
        db.session.commit()
        # Respond to the client
        return shop_schema.dump(shop), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Shop name already exist"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}, 409
        
