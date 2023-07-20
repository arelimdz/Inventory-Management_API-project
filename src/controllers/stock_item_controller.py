from flask import Blueprint, request
from init import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.stock_item import Stock_item, stock_item_schema, stock_items_schema
from models.user import User
import functools

stock_items_bp = Blueprint("stock_items", __name__, url_prefix="/stock_items")


@stock_items_bp.route("/")
def get_all_stock_items():
    stmt = db.select(Stock_item).order_by(Stock_item.category)
    stock_items = db.session.scalars(stmt)
    return stock_items_schema.dump(stock_items)


@stock_items_bp.route("/<int:id>")
def get_one_stock_item(id):
    stmt = db.select(Stock_item).filter_by(id=id)
    stock_item = db.session.scalar(stmt)
    if stock_item:
        return stock_item_schema.dump(stock_item)
    else:
        return {"error": f"Item with id {id} not found"}, 404


@stock_items_bp.route("/new_item", methods=["POST"])
@jwt_required()
def add_new_item():
    # Access to the information from the frontend and stored it in the variable body_data
    body_data = stock_item_schema.load(request.get_json())

    # Create a new Stock_item model instance
    stock_item = Stock_item(
        item_name=body_data.get("item_name"),
        item_description=body_data.get("item_description"),
        item_brand=body_data.get("item_brand"),
        size=body_data.get("size"),
        category=body_data.get("category"),
        quantity=body_data.get("quantity"),
        unit_price=body_data.get("unit_price"),
        markup_pct=body_data.get("markup_pct"),
        minimum_stock=body_data.get("minimum_stock"),
        sku=body_data.get("sku"),
        special_tax=body_data.get("special_tax"),
        status=body_data.get("status"),
    )
    # Add that stock item to the session
    db.session.add(stock_item)
    # Commit
    db.session.commit()
    # Respond to the client
    return stock_item_schema.dump(stock_item), 201
