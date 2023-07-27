from flask import Blueprint, request
from init import db
from sqlalchemy import exists
from flask_jwt_extended import jwt_required
from models.receipt import Receipt
from models.stock_item import StockItem, stock_item_schema
from models.outgoing_stock import (
    OutgoingStock,
    outgoing_stocks_schema,
    outgoing_stock_schema,
)

# from controllers.auth_controller import authorise_as_admin
from datetime import date

outgoing_stocks_blueprint = Blueprint(
    "outgoing_stock", __name__, url_prefix="/outgoingStocks"
)


@outgoing_stocks_blueprint.route("/", methods=["GET"])
def get_all_outgoing_stock():
    stmt = db.select(OutgoingStock).order_by(OutgoingStock.id)
    outgoing_stock = db.session.scalars(stmt)
    return outgoing_stocks_schema.dump(outgoing_stock)


@outgoing_stocks_blueprint.route("/<int:id>", methods=["GET"])
def get_one_outgoing_stock(id):
    stmt = db.select(OutgoingStock).filter_by(id=id)
    outgoing_stock = db.session.scalar(stmt)
    if outgoing_stock:
        return outgoing_stock_schema.dump(outgoing_stock)
    else:
        return {"error": f"OutgoingStock with id {id} not found"}, 404


@outgoing_stocks_blueprint.route("/item/<item_id>", methods=["GET"])
def get_item_price(item_id):
    stmt = db.select(StockItem).filter_by(id=item_id)
    item = db.session.scalar(stmt)
    price = item.unit_price
    quantity_in_stock = item.quantity
    return {"price": price, "quantity_in_stock": quantity_in_stock}


# Create a new OutgoingStock event
@outgoing_stocks_blueprint.route("/receipts/<id>", methods=["POST"])
# @jwt_required()
def add_outgoing_stock_event(id):
    # Check if receipt exists in receipts db
    receipt_exists = db.session.query(exists().where(Receipt.id == id)).scalar()
    receipt = Receipt.query.get(id)

    if receipt_exists and receipt.status == "Active":
        # Access frontend data
        body_data = outgoing_stock_schema.load(request.get_json())
        item_id = body_data.get("stock_item_id")
        quantity_wanted = body_data.get("quantity")

        # Check if item_id exists in database
        if item_id and quantity_wanted:
            item_exists = db.session.query(
                exists().where(StockItem.id == item_id)
            ).scalar()
            if item_exists:
                item = StockItem.query.get(item_id)
                quantity_in_stock = item.quantity
                price = item.unit_price
                tax = item.special_tax / 100
                item_status = item.status

                # Check if the item is currently active (not discontinued item)
                if item_status == "Active":
                    # Check if there are enough stock for sell
                    if quantity_in_stock >= quantity_wanted:
                        # Create a new OutgoingStock model instance using frontend data
                        outgoing_stock = OutgoingStock(
                            quantity=body_data.get("quantity"),
                            stock_item_id=item_id,
                            receipt_id=id,
                            subtotal=(price * quantity_wanted)
                            + ((tax * price) * quantity_wanted),
                        )
                        # Add that outgoing_stock to the session
                        db.session.add(outgoing_stock)
                        # Commit session
                        db.session.commit()

                        # Respond to the client
                        return outgoing_stock_schema.dump(outgoing_stock), 201
                    else:
                        return {
                            "error": f"Insufficient stock, {quantity_in_stock} pieces left"
                        }, 400
                else:
                    return {"error": f"Item with id {item_id} is discontinued"}
            else:
                return {"error": f"Item with id {item_id} not found"}, 404
        else:
            return {"error": "Item id and quantity required"}, 409
    else:
        return {"error": f"Receipt with id {id} not found or has been cancelled"}, 404
