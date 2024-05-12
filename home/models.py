from flask_login import UserMixin
from sqlalchemy.sql import func 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask import current_app
from home import db 
from forms import RegistrationForm, LoginForm

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable =False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='deafult.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"