from flask import Flask, Blueprint

profile_page = Blueprint('catprofile',__name__)

@profile_page.route('/catprofile')
def profile_page():
    return '<h1>Cat Profile</h1>'