from flask import Flask,Blueprint

profiledisplay = Blueprint('profiledisplay',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'hshshshsh'