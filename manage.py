from flask import Flask
from flask_migrate import Migrate
from models import db
from app import app   # import the app you already built

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
