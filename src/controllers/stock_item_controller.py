from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.stock_item import StockItem, stock_item_schema, stock_items_schema
from controllers.auth_controller import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

stock_items_blueprint = Blueprint("stockItems", __name__, url_prefix="/stockItems")


@stock_items_blueprint.route("/")
def get_all_stock_items():
    stmt = db.select(StockItem).order_by(StockItem.category)
    stock_items = db.session.scalars(stmt)
    return stock_items_schema.dump(stock_items)


@stock_items_blueprint.route("/<int:id>", methods=["GET"])
def get_one_stock_item(id):
    stmt = db.select(StockItem).filter_by(id=id)
    stock_item = db.session.scalar(stmt)
    if stock_item:
        return stock_item_schema.dump(stock_item)
    else:
        return {"error": f"Item with id {id} not found"}, 404


@stock_items_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_new_item():
    # Check if user has authorisation to performe action
    is_admin = authorise_as_admin()
    if not is_admin:
        return {"error": "Only Shop Manager can add new stock item"}, 403
    try:
        # Access to the information from the frontend
        body_data = stock_item_schema.load(request.get_json())
        # Check if item with sku same as user new item sku already exist in db
        stmt = db.select(StockItem).filter_by(sku="sku")
        stock_item = db.session.scalar(stmt)
        # If sku doesn't match with any other in db,
        if not stock_item:
            # Create a new StockItem model instance
            stock_item = StockItem(
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
                shop_id=body_data.get("shop_id"),
            )
            # Add the stock item to the session
            db.session.add(stock_item)
            # Commit the transaction to the database
            db.session.commit()
            # Respond to the client with the newly created stock item
            return stock_item_schema.dump(stock_item), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "SKU already exist"}, 409

        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}, 409


# Update information about an item in stock_items table
@stock_items_blueprint.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_stock_item(id):
    # Access to the information from the frontend
    body_data = stock_item_schema.load(request.get_json(), partial=True)
    # Check if stock item exist in db
    stmt = db.select(StockItem).filter_by(id=id)
    stock_item = db.session.scalar(stmt)
    # If item exist and user is admin update stock_item
    if stock_item:
        is_admin = authorise_as_admin()
        if not is_admin:
            return {"error": "Only Shop Manager can edit stock items"}, 403

        stock_item.item_name = body_data.get("item_name") or stock_item.item_name
        stock_item.item_description = (
            body_data.get("item_description") or stock_item.item_description
        )
        stock_item.item_brand = body_data.get("item_brand") or stock_item.item_brand
        stock_item.size = body_data.get("size") or stock_item.size
        stock_item.sku = body_data.get("sku") or stock_item.sku
        stock_item.category = body_data.get("category") or stock_item.category
        # stock_item.quantity = body_data.get("quantity") or stock_item.quantity
        stock_item.unit_price = body_data.get("unit_price") or stock_item.unit_price
        stock_item.markup_pct = body_data.get("markup_pct") or stock_item.markup_pct
        stock_item.minimum_stock = (
            body_data.get("minimum_stock") or stock_item.minimum_stock
        )
        stock_item.special_tax = body_data.get("special_tax") or stock_item.special_tax
        stock_item.status = body_data.get("status") or stock_item.status
        db.session.commit()
        return stock_item_schema.dump(stock_item)
    else:
        return {"error": f"Stock Item with id {id} not found"}, 404
