from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.customer import Customer, customer_schema, customers_schema
from controllers.auth_controller import authorise_as_admin

customers_blueprint = Blueprint("customers", __name__, url_prefix="/customers")


@customers_blueprint.route("/", methods=["GET"])
def get_all_customers():
    stmt = db.select(Customer).order_by(Customer.id)
    customers = db.session.scalars(stmt)
    return customers_schema.dump(customers)


@customers_blueprint.route("/<int:id>", methods=["GET"])
def get_one_customers(id):
    stmt = db.select(Customer).filter_by(id=id)
    customer = db.session.scalar(stmt)
    if customer:
        return customer_schema.dump(customer)
    else:
        return {"error": f"Customer with id {id} not found"}, 404


@customers_blueprint.route("/", methods=["POST"])
@jwt_required()
def add_new_customer():
    # Check if user is admin
    is_admin = authorise_as_admin()
    if not is_admin:
        return {"error": "Only The Shop Manager can register new customers"}, 403

    # Access to the information from the frontend and
    # stored it in the variable body_data
    body_data = customer_schema.load(request.get_json())

    # Create a new Customer model instance
    customer = Customer(
        name=body_data.get("name"),
        email=body_data.get("email"),
        address=body_data.get("address"),
        city=body_data.get("city"),
        phone_number=body_data.get("phone_number"),
        authorised_discount=body_data.get("authorised_discount"),
    )
    # Add that customer to the session
    db.session.add(customer)
    # Commit
    db.session.commit()
    # Respond to the client
    return customer_schema.dump(customer), 201
