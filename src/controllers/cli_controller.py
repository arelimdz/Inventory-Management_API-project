from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.stock_item import StockItem

db_commands = Blueprint("db", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables Created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command("seed")
def seed_db():
    users = [
        User(
            name="Owner",
            email="admin@admin.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="Manager",
            is_admin=True,
        ),
        User(
            name="Staff1",
            email="staff1@email.com",
            password=bcrypt.generate_password_hash("staff1123").decode("utf-8"),
            role="Sales Assistant",
        ),
    ]
    db.session.add_all(users)

    stock_items = [
        StockItem(
            item_name="Wash&Wear White",
            item_description="Low Sheen water-base paint for interior walls",
            item_brand="Dulux",
            size="1L",
            category="Water-based paint",
            quantity=24,
            unit_price=39.90,
            markup_pct=15.0,
            minimum_stock=50,
            sku="DWBWW100WH",
        ),
        StockItem(
            item_name="Super Enamel White",
            item_description="Semi Gloss is a high quality and hard-wearing oil-based interior enamel",
            item_brand="Dulux",
            size="4L",
            category="Oil-based paint",
            quantity=12,
            unit_price=89.90,
            markup_pct=10.0,
            minimum_stock=24,
            sku="DOBSE400WH",
            special_tax=15,
            status="Discontinued",
        ),
    ]
    db.session.add_all(stock_items)
    db.session.commit()

    print("Tables seeded")
