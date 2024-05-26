from flask import Flask,Blueprint

edit_profile = Blueprint('edit_profile',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'jfksfsfjkdnwieh'