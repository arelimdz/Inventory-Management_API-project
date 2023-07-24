from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.stock_item import StockItem, stock_item_schema, stock_items_schema
from controllers.auth_controller import authorise_as_admin
from models.shop import Shop, shop_schema, shops_schema


shops_blueprint = Blueprint("shop", __name__, url_prefix="/shops")


# Return information af all shop including all shop users
@shops_blueprint.route("/", methods=["GET"])
def get_all_shops():
    stmt = db.select(Shop)
    shops = db.session.scalars(stmt)
    return shops_schema.dump(shops)


# Return information of a single shop
@shops_blueprint.route("/<int:id>", methods=["GET"])
def get_one_shop(id):
    stmt = db.select(Shop).filter_by(id=id)
    shop = db.session.scalar(stmt)
    if shop:
        return shop_schema.dump(shop)
    else:
        return {"error": f"Shop with id {id} not found"}

