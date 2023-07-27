from flask import Blueprint, request
from init import db
from datetime import date
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
def get_all_incoming_stocks():
    stmt = db.select(IncomingStock).order_by(IncomingStock.id)
    incoming_stock = db.session.scalars(stmt)
    return incoming_stocks_schema.dump(incoming_stock)


@incoming_stocks_blueprint.route("/<int:id>", methods=["GET"])
def get_one_incoming_stock(id):
    stmt = db.select(IncomingStock).filter_by(id=id)
    incoming_stock = db.session.scalar(stmt)
    if incoming_stock:
        return incoming_stock_schema.dump(incoming_stock)
    else:
        return {"error": f"Incoming Stock with id {id} not found"}, 404


@incoming_stocks_blueprint.route("/", methods=["POST"])
def add_new_incoming_stock():
    try:
        # Access to the information from the frontend
        body_data = incoming_stock_schema.load(request.get_json())
        item_id = body_data.get("stock_item_id")
        # Check if stock_item exist in db
        stmt = db.select(StockItem).filter_by(id=item_id)
        stock_item = db.session.scalar(stmt)

        if stock_item:
            # Create a new IncomingStock model instance
            incoming_stock = IncomingStock(
                date=date.today(),
                quantity=body_data.get("quantity"),
                item_cost=body_data.get("item_cost"),
                invoice_number=body_data.get("invoice_number"),
                supplier_id=body_data.get("supplier_id"),
                stock_item_id=body_data.get("stock_item_id"),
            )
            # Add the incoming_stock to the session
            db.session.add(incoming_stock)
            # Update quantity in stock_item database
            stock_item.quantity = stock_item.quantity + body_data.get("quantity")
            # Commit changes to the database
            db.session.commit()
            # Respond to the client with the newly created stock item
            return incoming_stock_schema.dump(incoming_stock), 201
        else:
            return {
                "error": f"Item with id {item_id} not found, You need to register new item"
            }
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"}, 409
