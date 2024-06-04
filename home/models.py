from flask_login import UserMixin, current_user
from sqlalchemy.sql import func 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from flask import current_app
from home import db 
from .forms import SignUpForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password1 = db.Column(db.String(255), nullable=False)
    password2 = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phonenumber = db.Column(db.String(20), unique=True, nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('Like', backref='author', lazy=True)
    cats = db.relationship('Cat', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}', '{self.username}', '{self.state}', '{self.phonenumber}')"
    
class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100), nullable=False)
    cat_photo = db.Column(db.String(255), nullable=True)
    cat_age = db.Column(db.Integer, nullable=False)
    cat_breed = db.Column(db.String(100), nullable=False)
    cat_gender = db.Column(db.String(10), nullable=False)
    cat_neutered = db.Column(db.String(10), nullable=False)
    cat_vaccine = db.Column(db.String(10), nullable=False)
    cat_special_needs = db.Column(db.String(100), nullable=False)
    cat_about_me = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    available_for_adoption = db.Column(db.Boolean, default=False)
    date_put_for_adoption = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Cat('{self.cat_name}','{self.cat_photo}', '{self.cat_age}','{self.cat_breed}','{self.cat_gender}','{self.cat_neutered}','{self.cat_vaccine}','{self.cat_special_needs}','{self.cat_about_me}', '{self.available_for_adoption}'))"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable =False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file = db.Column(db.String(255), nullable=True)
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    #user = db.relationship('User', backref='user_comments')
    #post = db.relationship('Post', backref='post_comments')

    def __repr__(self):
        return f"Comment('{self.text}', '{self.date}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    notification_type = db.Column(db.String(20),nullable=False)
    time = db.Column(db.DateTime, default=func.now())
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Notification {self.id}>"