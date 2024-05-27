from flask import Flask,Blueprint

user_edit = Blueprint('user_edit',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'jfksfsfjkdnwieh'