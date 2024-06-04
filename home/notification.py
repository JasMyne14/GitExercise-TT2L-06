from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit
from .user_posts import *
from .models import db,User

notification = Blueprint('notification',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'notifications'
