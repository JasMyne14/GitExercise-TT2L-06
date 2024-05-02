from flask import Blueprint

registercat = Blueprint('registercat',__name__)

@registercat.route('/catregister')
def registercat():
    return '<h1>Register your cat here!</h1>'