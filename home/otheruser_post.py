from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit
from .user_posts import *
from .models import db,User

otheruser_post = Blueprint('otheruser_post',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'otheruser_post'
