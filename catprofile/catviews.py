from flask import Blueprint

viewscat = Blueprint('viewscat', __name__)

@viewscat.route('/')
def catviews():
    return "<h1>Test</h1>"

#@viewscat.route('/catprofile')
#def profile_page():
#    return "<h1>Cat Profile</h1>"

