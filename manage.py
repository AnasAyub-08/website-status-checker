from flask.cli import FlaskGroup
from flask_migrate import Migrate
from models import db
from app import app   # import the app you already built

migrate = Migrate(app, db)
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
