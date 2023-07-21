from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_blueprint
from controllers.stock_item_controller import stock_items_blueprint


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register all blueprints that exist in the app
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(stock_items_blueprint)
    return app
