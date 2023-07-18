from flask import Blueprint
from init import db, bcrypt
from models.user import User

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
            role="Sales Assistant"
        ),
    ]
    db.session.add_all(users)
    db.session.commit()

    print("Tables seeded")

