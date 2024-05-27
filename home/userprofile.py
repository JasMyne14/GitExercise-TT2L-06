from flask import Flask,Blueprint

userprofile = Blueprint('userprofile',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'jfksfsfjkdnwieh'
