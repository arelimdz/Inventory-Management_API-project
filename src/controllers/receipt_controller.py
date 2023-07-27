from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.receipt import Receipt, receipt_schema, receipts_schema

# from controllers.auth_controller import authorise_as_admin
from datetime import date

receipts_blueprint = Blueprint("receipts", __name__, url_prefix="/receipts")


@receipts_blueprint.route("/", methods=["GET"])
def get_all_receipts():
    stmt = db.select(Receipt).order_by(Receipt.id)
    receipts = db.session.scalars(stmt)
    return receipts_schema.dump(receipts)


# @receipts_blueprint.route("/<int:id>", methods=["GET"])
# def get_one_receipts(id):
#     stmt = db.select(Receipt).filter_by(id=id)
#     receipt = db.session.scalar(stmt)

#     if receipt:
#         # Calculate the total based on the subtotal of each outgoing stock item
#         total = sum(
#             outgoing_stock.subtotal for outgoing_stock in receipt.outgoing_stocks
#         )

#         # Update the receipt's total in the database
#         receipt.total = total
#         db.session.commit()

#         # Serialize the receipt and include the outgoing stock subtotals
#         serialized_receipt = receipt_schema.dump(receipt)
#         return serialized_receipt
#     else:
#         return {"error": f"Receipt with id {id} not found"}, 404


# @receipts_blueprint.route("/<int:id>", methods=["GET"])
# def get_one_receipts(id):
#     stmt = db.select(Receipt).filter_by(id=id)
#     receipt = db.session.scalar(stmt)

#     if receipt:
#         # Calculate the product total based on the subtotal of each outgoing stock item
#         items_total = sum(
#             outgoing_stock.subtotal for outgoing_stock in receipt.outgoing_stocks
#         )

#         # Calculate customer's discount

#         total = items_total

#         # Update the receipt's total in the database
#         receipt.total = total
#         db.session.commit()

#         # Serialize the receipt and include the outgoing stock subtotals
#         serialized_receipt = receipt_schema.dump(receipt)
#         return serialized_receipt
#     else:
#         return {"error": f"Receipt with id {id} not found"}, 404


@receipts_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_new_receipt():
    # Access to frontend data
    body_data = receipt_schema.load(request.get_json())

    # Create a new Receipt model instance using frontend data
    receipt = Receipt(
        payment_method=body_data.get("payment_method"),
        purchase_type=body_data.get("purchase_type"),
        customer_id=body_data.get("customer_id"),
        date=date.today(),
    )
    # Add that receipt to the session
    db.session.add(receipt)
    # Commit session
    db.session.commit()
    # Respond to the client
    return receipt_schema.dump(receipt), 201
