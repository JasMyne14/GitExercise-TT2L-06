from flask import Flask,Blueprint

registercat = Blueprint('catregister',__name__)

@registercat.route('/catregister')
def registercat():
    return '<h1>register your cat here!</h1>'