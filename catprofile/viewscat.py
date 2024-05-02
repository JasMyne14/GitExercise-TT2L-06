from flask import Flask, Blueprint, render_template

viewscat = Blueprint('viewscat', __name__)

@viewscat.route('/')
def home():
    return render_template('base.html')

@viewscat.route('/viewscat')
def catviews():
    return "<h1>View cat page </h1>"

@viewscat.route('/registercat')
def registercat():
    return '<h1>Register your cat here!</h1>'

@viewscat.route('/profile_page')
def profile_page():
    return '<h1>Cat Profile</h1>'
