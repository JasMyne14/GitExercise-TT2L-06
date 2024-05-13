from flask import Flask,Blueprint, request, redirect, url_for, render_template
from .models import db, User
from flask import flash
import os

signup = Blueprint('signup',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'hshshshsh'

@signup.route('/signup', methods=['POST'])
def signup():
    fullname = request.form['fullname']
    email = request.form['email']
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    state = request.form['state']
    phonenumber = request.form['phonenumber']
    
    if password1 != password2:
        flash('Passwords do not match', 'error')
        return redirect(url_for('signup'))
    
    if User.query.filter_by(email=email).first():
        flash('Email already exists', 'error')
        return redirect(url_for('signup'))
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'error')
        return redirect(url_for('signup'))
    
    hashed_password = generate_password_hash(password1)


    new_signup = User(fullname=fullname,
                  email=email,
                  username=username,
                  password1=password1,
                  password2=password2,
                  state=state,
                  phonenumber=phonenumber)
    
    db.session.add(new_signup)
    db.session.commit()

    flash('Signup Successful !', 'success')
    return redirect(url_for('views.mainpage'))
