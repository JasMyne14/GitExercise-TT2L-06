from flask import Blueprint

cats = Blueprint('cats',__name__)

@cats.route('/')
def house():
    return 'testing'