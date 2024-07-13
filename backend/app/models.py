# This file will hold your database models
# Example using SQLAlchemy (optional, only if using a database)

from flask_sqlalchemy import SQLAlchemy
from . import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
