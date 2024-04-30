from flask import Flask, Blueprint

catprofile = Blueprint('catprofile',__name__)

@catprofile.route('/catprofile')
def catprofile():
    return '<h1>cat profile</h1>'