from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)

    # Delete all websites (and their logs) when user is deleted
    websites = db.relationship(
        "Website",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), default="Unknown")
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Delete logs when website is deleted
    logs = db.relationship(
        "StatusLog",
        backref="website",
        cascade="all, delete-orphan"
    )


class StatusLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(
        db.Integer,
        db.ForeignKey("website.id", ondelete="CASCADE"),
        nullable=False
    )
    status = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
