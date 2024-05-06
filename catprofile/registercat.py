from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .models import db, CatForm

registercat = Blueprint('registercat', __name__)

@registercat.route('/register', methods=['POST'])
def register():
    name = request.form['cat_name']
    breed = request.form['breed']
    age = request.form['age']
    gender = request.form['gender']
    neutered = request.form['neutered']
    vaccine = request.form['vaccine']
    special_needs = request.form['special_needs']
    about_me = request.form['about_me']
    owner_name = request.form['owner_name']
    owner_email = request.form['owner_email']
    owner_contact = request.form['owner_contact']

    formcat = CatForm(name=name, breed=breed, age=age, gender=gender, neutered=neutered, vaccine=vaccine, special_needs=special_needs, about_me=about_me, owner_name=owner_name, owner_email=owner_email, owner_contact=owner_contact)
    db.session.add(formcat)
    db.session.commit()

    return redirect(url_for('viewscat.home'))

