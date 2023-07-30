from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_blueprint
from controllers.stock_item_controller import stock_items_blueprint
from controllers.customer_controller import customers_blueprint
from controllers.shop_controller import shops_blueprint
from controllers.supplier_controller import suppliers_blueprint
from controllers.receipt_controller import receipts_blueprint
from controllers.outgoing_stock_controller import outgoing_stocks_blueprint
from controllers.incoming_stock_controller import incoming_stocks_blueprint
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register all blueprints that exist in the app
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(stock_items_blueprint)
    app.register_blueprint(customers_blueprint)
    app.register_blueprint(shops_blueprint)
    app.register_blueprint(suppliers_blueprint)
    app.register_blueprint(receipts_blueprint)
    app.register_blueprint(outgoing_stocks_blueprint)
    app.register_blueprint(incoming_stocks_blueprint)

    return app
