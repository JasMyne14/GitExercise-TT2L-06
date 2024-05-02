from flask import Blueprint

profile_page = Blueprint('profile_page',__name__)

@profile_page.route('/catprofile')
def profile_page():
    return '<h1>Cat Profile</h1>'