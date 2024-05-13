from flask import Flask,Blueprint, request, redirect, url_for, render_template
from .models import db, User
from flask import flash
import os

signup = Blueprint('signup',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'hshshshsh'

@signup.route('/signup', methods=['GET','POST'])
def signup():
    fullname = request.form['fullname']
    email = request.form['email']
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    state = request.form['state']
    phonenumber = request.form['phonenumber']

    signup = User(fullname=fullname,
                  email=email,
                  username=username,
                  password1=password1,
                  password2=password2,
                  state=state,
                  phonenumber=phonenumber)
    
    db.session.add(signup)
    db.session.commit()

    return redirect(url_for('views.mainpage'))
