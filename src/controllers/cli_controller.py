from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.stock_item import StockItem
from models.customer import Customer
from models.shop import Shop
from models.supplier import Supplier
from models.receipt import Receipt
from models.outgoing_stock import OutgoingStock
from models.incoming_stock import IncomingStock


db_commands = Blueprint("db", __name__)

# Create cli commands to test Models


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables Created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")


# Insert test data to test Models
@db_commands.cli.command("seed")
def seed_db():
    shops = [
        Shop(
            shop_name="The Painter house",
            address="The corner St, Melbourne",
            description="Retail paint shop specialising in car paints",
        ),
        Shop(
            shop_name="Random Paint Shop",
            address="Somewhere far away St, Adelaide",
            description="Retail shop for all kinds of paints",
        ),
    ]
    db.session.add_all(shops)

    users = [
        User(
            name="Owner",
            email="admin@admin.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="Manager",
            is_admin=True,
            shop=shops[0],
        ),
        User(
            name="Staff1",
            email="staff1@email.com",
            password=bcrypt.generate_password_hash("staff1123").decode("utf-8"),
            role="Sales Assistant",
            shop=shops[0],
        ),
    ]
    db.session.add_all(users)

    stock_items = [
        StockItem(
            item_name="Wash&Wear White",
            item_description="Low Sheen, water-base, for interior walls",
            item_brand="Dulux",
            size="1L",
            category="Water-based",
            quantity=100,
            unit_cost=10,
            unit_price=11,
            markup_pct=10,
            minimum_stock=50,
            sku="DWBWW100WH",
            shop=shops[0],
        ),
        StockItem(
            item_name="Wash&Wear Beige",
            item_description="Low Sheen, water-base, for interior walls",
            item_brand="Dulux",
            size="4L",
            category="Water-based",
            quantity=50,
            unit_cost=20,
            unit_price=22,
            markup_pct=10,
            minimum_stock=20,
            sku="DWBWW400BG",
            shop=shops[0],
        ),
        StockItem(
            item_name="UltraColor Green",
            item_description="Low Sheen, water-base, for exterior walls",
            item_brand="Dulux",
            size="19L",
            category="Water-based",
            quantity=10,
            unit_cost=200,
            unit_price=220,
            markup_pct=10,
            minimum_stock=10,
            sku="DWBUC1900GR",
            shop=shops[0],
        ),
        StockItem(
            item_name="Super-Enamel White",
            item_description="Semi Gloss, oil-based interior enamel",
            item_brand="Dulux",
            size="4L",
            category="Oil-based",
            quantity=50,
            unit_cost=80,
            unit_price=92.00,
            markup_pct=15,
            minimum_stock=24,
            sku="DOBSE400WH",
            special_tax=15,
            status="Discontinued",
            shop=shops[1],
        ),
        StockItem(
            item_name="Acrilac Black",
            item_description="Super Gloss acrilic paint",
            item_brand="Sherwin-Williams",
            size="0.250L",
            category="Acrilic",
            quantity=100,
            unit_cost=10,
            unit_price=11,
            markup_pct=10,
            minimum_stock=25,
            sku="SWABAC250BL",
            shop=shops[1],
        ),
        StockItem(
            item_name="Super-Car Red",
            item_description="Super Gloss car paint",
            item_brand="Sherwin-Williams",
            size="4L",
            category="Polyurethane",
            quantity=20,
            unit_cost=1500,
            unit_price=1800,
            markup_pct=20,
            minimum_stock=25,
            sku="SWPBSC400RE",
            shop=shops[1],
        ),
    ]
    db.session.add_all(stock_items)

    customers = [
        Customer(
            name="David Lee",
            email="dlee@email.com",
            address="Example St",
            city="Melbourne",
            phone_number="00112233",
            authorised_discount=5.0,
        ),
        Customer(
            name="Margaret Milo",
            email="mmilo@email.com",
            address="Example Av",
            city="Geelong",
            phone_number="44556677",
        ),
    ]
    db.session.add_all(customers)

    suppliers = [
        Supplier(
            name="Dulux Company",
            email="dulux_supplier@email.com",
            phone_number="123987",
            address="Dulux St, Melbourne",
        ),
        Supplier(
            name="Sherwin-Williams",
            email="sw_supplier@email.com",
            phone_number="987098",
            address="Creations St, Sydney",
        ),
    ]
    db.session.add_all(suppliers)

    receipts = [
        Receipt(
            # date=date.today(),
            subtotal=100,
            discount=24,
            total=76.0,
            payment_method="Card",
            purchase_type="Credit",
            customer=customers[0],
        ),
        Receipt(
            # date=date.today(),
            subtotal=23.57,
            discount=0,
            total=23.57,
            payment_method="Cash",
            purchase_type="One-off payment",
            customer=customers[0],
        ),
    ]
    db.session.add_all(receipts)

    outgoing_stocks = [
        OutgoingStock(
            stock_item=stock_items[0],
            quantity=1,
            receipt=receipts[1],
            subtotal=23.57,
            tax=2.7,
            total=26.27,
        )
    ]
    db.session.add_all(outgoing_stocks)

    incoming_stocks = [
        IncomingStock(
            quantity=10,
            item_cost=17.42,
            stock_item=stock_items[1],
            invoice_number="D-000",
            supplier=suppliers[1],
        )
    ]
    db.session.add_all(incoming_stocks)

    db.session.commit()

    print("Tables seeded")
