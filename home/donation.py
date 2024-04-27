from flask import Flask,Blueprint

about = Blueprint('about',__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'love'


