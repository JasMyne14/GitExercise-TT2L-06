from flask import Flask,Blueprint

catregister = Blueprint('catregister',__name__)

@catregister.route('/catregister')
def catregister():
    return 'register your cat here!'