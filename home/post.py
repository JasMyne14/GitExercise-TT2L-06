from flask import Flask,Blueprint,render_template,redirect,request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from .__init__ import *
from home import create_app

post = Blueprint('post',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'love'
