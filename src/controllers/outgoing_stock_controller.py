from flask import Blueprint, request
from init import db
from sqlalchemy import exists
from flask_jwt_extended import jwt_required
from models.receipt import Receipt
from models.stock_item import StockItem
from controllers.auth_controller import authorise_as_admin
from models.outgoing_stock import (
    OutgoingStock,
    outgoing_stocks_schema,
    outgoing_stock_schema,
)


outgoing_stocks_blueprint = Blueprint(
    "outgoing_stock", __name__, url_prefix="/outgoingStocks"
)


@outgoing_stocks_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_all_outgoing_stock():
    stmt = db.select(OutgoingStock).order_by(OutgoingStock.id)
    outgoing_stock = db.session.scalars(stmt)
    return outgoing_stocks_schema.dump(outgoing_stock)


@outgoing_stocks_blueprint.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_one_outgoing_stock(id):
    stmt = db.select(OutgoingStock).filter_by(id=id)
    outgoing_stock = db.session.scalar(stmt)
    if outgoing_stock:
        return outgoing_stock_schema.dump(outgoing_stock)
    else:
        return {"error": f"OutgoingStock with id {id} not found"}, 404


# This route create a new outgoing_stock event and update stock_items table
@outgoing_stocks_blueprint.route("/receipts/<id>", methods=["POST"])
@jwt_required()
def add_outgoing_stock_event(id):
    # Check if receipt exists in receipts db
    receipt_exists = db.session.query(exists().where(Receipt.id == id)).scalar()
    receipt = Receipt.query.get(id)

    if receipt_exists and receipt.is_active:
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
                # Access to stock_items table
                stmt = db.select(StockItem).filter_by(id=item_id)
                item = db.session.scalar(stmt)

                # item = StockItem.query.get(item_id)
                quantity_in_stock = item.quantity
                price = item.unit_price
                total_tax = price * (item.special_tax / 100)
                item_status = item.status
                item_subtotal = price * quantity_wanted

                # Check if the item is currently active (not discontinued item)
                if item_status == "Active":
                    # Check if there are enough stock for sell
                    if quantity_in_stock >= quantity_wanted:
                        # Create a new OutgoingStock model instance using frontend data
                        outgoing_stock = OutgoingStock(
                            quantity=body_data.get("quantity"),
                            stock_item_id=item_id,
                            receipt_id=id,
                            subtotal=item_subtotal,
                            tax=total_tax,
                            total=item_subtotal + total_tax,
                        )

                        # Update the stock_items's quantity in the database
                        item.quantity -= quantity_wanted

                        # Add that outgoing_stock to the session
                        db.session.add(outgoing_stock)

                        # Commit all changes in session
                        db.session.commit()

                        # Respond to the client
                        return outgoing_stock_schema.dump(outgoing_stock), 201
                    else:
                        return {
                            "error": f"Insufficient stock, {quantity_in_stock} pieces left"
                        }, 400
                else:
                    return {"error": f"Item with id {item_id} is discontinued"}, 400
            else:
                return {"error": f"Item with id {item_id} not found"}, 404
        else:
            return {"error": "Item id and quantity required"}, 409
    else:
        return {"error": f"Receipt with id {id} not found or has been cancelled"}, 404


# This route delete outgoing_stock and update stock_item
@outgoing_stocks_blueprint.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_one_card(id):
    # Check if user is admin
    is_admin = authorise_as_admin()
    if not is_admin:
        return {"error": "Only Shop Manager can delete outgoing_stock events"}, 403

    # Check if outgoing_stock id exist
    id_exists = db.session.query(exists().where(OutgoingStock.id == id)).scalar()

    if id_exists:
        # Access to outgoing_stock database
        outgoing_stock = OutgoingStock.query.get(id)
        item_id = outgoing_stock.stock_item_id
        add_quantity_back = outgoing_stock.quantity
        # Access to stock_items database
        stmt = db.select(StockItem).filter_by(id=item_id)
        item = db.session.scalar(stmt)

        # Update the stock_items's quantity in the database
        item.quantity += add_quantity_back

        # Delete outgoing stock event
        db.session.delete(outgoing_stock)

        # Commit changes to the database
        db.session.commit()

        # Respond to the client with a success message
        return {
            "message": f"Outgoing_stock event {outgoing_stock.id} deleted successfully"
        }
    else:
        return {"error": f"Outgoing_stock with id {id} not found"}, 404
