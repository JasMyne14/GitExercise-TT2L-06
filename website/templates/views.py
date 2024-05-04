from flask import  Blueprint

view = Blueprint('views', __name__)

@views.route('/')
def home():
    return "<h1>Test</h1>"