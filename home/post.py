from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy

form = Blueprint('form',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'form'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///app.db'
db = SQLAlchemy(app)

db.create_all()
