from flask import Blueprint, request
from init import db
from sqlalchemy import exists
from flask_jwt_extended import jwt_required
from models.stock_item import StockItem
from controllers.auth_controller import authorise_as_admin
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.incoming_stock import (
    IncomingStock,
    incoming_stock_schema,
    incoming_stocks_schema,
)


incoming_stocks_blueprint = Blueprint(
    "incoming_stock", __name__, url_prefix="/incomingStocks"
)


@incoming_stocks_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_all_incoming_stocks():
    stmt = db.select(IncomingStock).order_by(IncomingStock.id)
    incoming_stock = db.session.scalars(stmt)
    return incoming_stocks_schema.dump(incoming_stock)


@incoming_stocks_blueprint.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_one_incoming_stock(id):
    stmt = db.select(IncomingStock).filter_by(id=id)
    incoming_stock = db.session.scalar(stmt)
    if incoming_stock:
        return incoming_stock_schema.dump(incoming_stock)
    else:
        return {"error": f"Incoming Stock with id {id} not found"}, 404


# This route create a new incoming_stock event that update stock_items tables (quantity)
@incoming_stocks_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_new_incoming_stock():
    # Check if user is admin
    is_admin = authorise_as_admin()
    if not is_admin:
        return {"error": "Only Shop Manager can create incoming_stock events"}, 403

    try:
        # Access to the information from the frontend
        body_data = incoming_stock_schema.load(request.get_json())
        item_id = body_data.get("stock_item_id")
        invoice = body_data.get("invoice_number")
        new_cost = body_data.get("item_cost")

        # Check if stock_item exists in the database
        stock_item = StockItem.query.get(item_id)

        if stock_item:
            # Check if there is any price change
            if new_cost == stock_item.unit_cost:
                # Create a new IncomingStock model instance
                incoming_stock = IncomingStock(
                    quantity=body_data.get("quantity"),
                    item_cost=body_data.get("item_cost"),
                    invoice_number=invoice,
                    supplier_id=body_data.get("supplier_id"),
                    stock_item_id=item_id,
                )
                # Add the incoming_stock to the session
                db.session.add(incoming_stock)
                # Update quantity in stock_item database
                stock_item.quantity += body_data.get("quantity")
                # Commit changes to the database
                db.session.commit()
                # Respond to the client with the newly created stock item
                return incoming_stock_schema.dump(incoming_stock), 201
            else:
                return {
                    "message": f"There is a cost change on item with id {item_id}, you need to update item unit_cost"
                }, 422
        else:
            return {
                "error": f"Item with id {item_id} not found, You need to register a new item"
            }, 404
    except IntegrityError as err:
        # Check if incoming_stock event is not duplicate
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {
                "error": f"Item with id {item_id} has been registered with invoice number {invoice}"
            }, 409
        elif err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}, 400


# This route delete an incoming_stock event given the id and update stock_items tables (quantity)
@incoming_stocks_blueprint.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_incoming_stock(id):
    # Check if user is admin
    is_admin = authorise_as_admin()
    if not is_admin:
        return {"error": "Only Shop Manager can delete incoming_stock events"}, 403

    # Check if incoming stock exists in the database
    id_exists = db.session.query(exists().where(IncomingStock.id == id)).scalar()

    if id_exists:
        # Access to outgoing_stock database
        incoming_stock = IncomingStock.query.get(id)
        item_id = incoming_stock.stock_item_id
        remove_from_stock = incoming_stock.quantity

        # Access to stock_items database
        stmt = db.select(StockItem).filter_by(id=item_id)
        item = db.session.scalar(stmt)

        # Update the stock_items's quantity in the database
        item.quantity -= remove_from_stock

        # Delete outgoing stock event
        db.session.delete(incoming_stock)

        # Commit changes to the database
        db.session.commit()

        # Respond to the client with a success message
        return {
            "message": f"Incoming stock with id {id} has been deleted successfully"
        }, 200
    else:
        return {"error": f"Incoming stock with id {id} not found"}, 404
