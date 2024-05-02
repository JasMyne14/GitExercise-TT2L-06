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
    return render_template('catregister.html')

@viewscat.route('/profile_page')
def profile_page():
    return render_template('catprofile.html')
