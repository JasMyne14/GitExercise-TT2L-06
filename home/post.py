from flask import Flask,Blueprint,render_template,redirect,request, url_for, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length
from .__init__ import *
from home import create_app

post = Blueprint('post',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'love'

