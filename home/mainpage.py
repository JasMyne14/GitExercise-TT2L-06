from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit
from .user_posts import *

mainpage = Blueprint('mainpage',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'home'