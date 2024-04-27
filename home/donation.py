from flask import Flask,Blueprint

donation = Blueprint('donation',__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'love'


