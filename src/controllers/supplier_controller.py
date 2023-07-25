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


@suppliers_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_new_supplier():
    # Check if user is admin
    is_admin = authorise_as_admin()
    if not is_admin:
        return {"error": "Only Shop Manager can register new suppliers"}, 403

    # Access to frontend data
    body_data = supplier_schema.load(request.get_json())

    # Create a new Supplier model instance using frontend data
    supplier = Supplier(
        name=body_data.get("name"),
        email=body_data.get("email"),
        address=body_data.get("address"),
        phone_number=body_data.get("phone_number"),
    )
    # Add that supplier to the session
    db.session.add(supplier)
    # Commit session
    db.session.commit()
    # Respond to the client
    return supplier_schema.dump(supplier), 201

