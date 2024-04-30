from flask import Flask, Blueprint

catprofile = Blueprint('catprofile',__name__)

@catprofile.route('/catprofile')
def catprofile():
    return 'cat profile'