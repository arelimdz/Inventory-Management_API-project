from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.stock_item import StockItem, stock_item_schema, stock_items_schema
from models.user import User

stock_items_blueprint = Blueprint("stockItems", __name__, url_prefix="/stockItems")


@stock_items_blueprint.route("/")
def get_all_stock_items():
    stmt = db.select(StockItem).order_by(StockItem.category)
    stock_items = db.session.scalars(stmt)
    return stock_items_schema.dump(stock_items)


@stock_items_blueprint.route("/<int:id>")
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
    # Access to the information from the frontend and
    # stored it in the variable body_data
    body_data = stock_item_schema.load(request.get_json())

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
    )
    # Add that stock item to the session
    db.session.add(stock_item)
    # Commit
    db.session.commit()
    # Respond to the client
    return stock_item_schema.dump(stock_item), 201


# Update an item in stock_items table
@stock_items_blueprint.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_stock_item(id):
    # Access to the information from the frontend and
    # stored it in the variable body_data
    body_data = stock_item_schema.load(request.get_json(), partial=True)
    stmt = db.select(StockItem).filter_by(id=id)
    stock_item = db.session.scalar(stmt)

    if stock_item:
        is_admin = authorise_as_admin()
        if not is_admin:
            return {"error": "Only The Shop Manager can edit stock items"}, 403

        stock_item.item_name = body_data.get("item_name") or stock_item.item_name
        stock_item.item_description = (
            body_data.get("item_description") or stock_item.item_description
        )
        stock_item.item_brand = body_data.get("item_brand") or stock_item.item_brand
        stock_item.size = body_data.get("size") or stock_item.size
        stock_item.sku = body_data.get("sku") or stock_item.sku
        stock_item.category = body_data.get("category") or stock_item.category
        stock_item.quantity = body_data.get("quantity") or stock_item.quantity
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


def authorise_as_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin
