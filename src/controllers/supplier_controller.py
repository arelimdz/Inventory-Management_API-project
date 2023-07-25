from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.supplier import Supplier, supplier_schema, suppliers_schema
from controllers.auth_controller import authorise_as_admin

suppliers_blueprint = Blueprint("suppliers", __name__, url_prefix="/suppliers")


@suppliers_blueprint.route("/", methods=["GET"])
def get_all_suppliers():
    stmt = db.select(Supplier).order_by(Supplier.id)
    suppliers = db.session.scalars(stmt)
    return suppliers_schema.dump(suppliers)


@suppliers_blueprint.route("/<int:id>", methods=["GET"])
def get_one_suppliers(id):
    stmt = db.select(Supplier).filter_by(id=id)
    supplier = db.session.scalar(stmt)
    if supplier:
        return supplier_schema.dump(supplier)
    else:
        return {"error": f"Supplier with id {id} not found"}, 404

