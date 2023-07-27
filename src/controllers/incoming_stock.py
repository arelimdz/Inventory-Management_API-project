from flask import Blueprint, request
from init import db
from sqlalchemy import exists
from flask_jwt_extended import jwt_required
from models.receipt import Receipt
from models.stock_item import StockItem
from controllers.auth_controller import authorise_as_admin
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
