from flask import Flask,Blueprint

form = Blueprint('form',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'form'