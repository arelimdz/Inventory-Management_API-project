from flask import Blueprint, request
from init import db
from sqlalchemy import exists
from flask_jwt_extended import jwt_required
from models.receipt import Receipt, receipt_schema, receipts_schema
from models.customer import Customer
from controllers.auth_controller import authorise_as_admin
from datetime import date

receipts_blueprint = Blueprint("receipts", __name__, url_prefix="/receipts")


@receipts_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_all_receipts():
    stmt = db.select(Receipt).order_by(Receipt.id)
    receipts = db.session.scalars(stmt)
    return receipts_schema.dump(receipts)


@receipts_blueprint.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_one_receipts(id):
    stmt = db.select(Receipt).filter_by(id=id)
    receipt = db.session.scalar(stmt)

    if receipt:
        # Calculate receipt subtotal base in all products in receipt
        subtotal = sum(
            outgoing_stock.total for outgoing_stock in receipt.outgoing_stocks
        )

        # Calculate customer's discount
        customer = Customer.query.get(receipt.customer_id)
        discount = (customer.authorised_discount * subtotal) / 100

        total = subtotal - discount

        # Update the receipt's total in the database
        receipt.total = total
        receipt.discount = discount
        receipt.subtotal = subtotal
        db.session.commit()

        # Serialize the receipt and include the outgoing stock subtotals
        serialized_receipt = receipt_schema.dump(receipt)
        return serialized_receipt
    else:
        return {"error": f"Receipt with id {id} not found"}, 404


@receipts_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_new_receipt():
    # Access to frontend data
    body_data = request.get_json()

    # Create a new Receipt model instance using frontend data
    receipt = Receipt(
        payment_method=body_data.get("paymentMethod"),
        purchase_type=body_data.get("purchaseType"),
        customer_id=body_data.get("customerId"),
        date=date.today(),
    )
    # Add that receipt to the session
    db.session.add(receipt)
    # Commit session
    db.session.commit()
    # Respond to the client
    return receipt_schema.dump(receipt), 201


@receipts_blueprint.route("/<int:id>", methods=["PATCH", "PUT"])
@jwt_required()
def cancel_receipt(id):
    # Check if user is admin
    is_admin = authorise_as_admin()
    if not is_admin:
        return {"error": "Only Shop Manager can cancel receipts information"}, 403

    # Check if receipt exist
    receipt_exists = db.session.query(exists().where(Receipt.id == id)).scalar()
    receipt_status = Receipt.query.get(id)
    # Check if receipt is active
    if not receipt_status.is_active:
        return {"message": f"Receipt with id {id} has already been CANCELLED"}

    if receipt_exists and receipt_status.is_active:
        # Access to frontend data
        body_data = receipt_schema.load(request.get_json(), partial=True)
        stmt = db.select(Receipt).filter_by(id=id)
        receipt = db.session.scalar(stmt)
        # Update receipt is_active to FALSE
        receipt.is_active = body_data.get("is_active")
        # Add that receipt to the session
        db.session.add(receipt)
        # Commit session
        db.session.commit()
        # Respond to the client

        return {"message": f"Receipt with id {id} has been CANCELLED successfully"}, 200

    else:
        return {"error": f"Receipt with id {id} not found"}, 404
