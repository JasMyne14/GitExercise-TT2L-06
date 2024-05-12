from flask import Flask, Blueprint, render_template
from .models import CatForm
from flask import flash

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
    formcat = CatForm.query.all()
    return render_template('catprofile.html', fomrcat=formcat)
