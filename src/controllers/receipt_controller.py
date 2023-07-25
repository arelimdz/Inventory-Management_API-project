from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.receipt import Receipt, receipt_schema, receipts_schema
from controllers.auth_controller import authorise_as_admin


receipts_blueprint = Blueprint("receipts", __name__, url_prefix="/receipts")


@receipts_blueprint.route("/", methods=["GET"])
def get_all_receipts():
    stmt = db.select(Receipt).order_by(Receipt.id)
    receipts = db.session.scalars(stmt)
    return receipts_schema.dump(receipts)


@receipts_blueprint.route("/<int:id>", methods=["GET"])
def get_one_receipts(id):
    stmt = db.select(Receipt).filter_by(id=id)
    receipt = db.session.scalar(stmt)
    if receipt:
        return receipt_schema.dump(receipt)
    else:
        return {"error": f"Receipt with id {id} not found"}, 404

