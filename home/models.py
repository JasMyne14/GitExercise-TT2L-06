from flask_login import UserMixin
from sqlalchemy.sql import func 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask import current_app
from home import db 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable =False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
