from flask import Blueprint, request, redirect, url_for,flash
from .models import db, RegisterCat
from werkzeug.utils import secure_filename
import os

registercat = Blueprint('registercat', __name__)

upload_folder = 'home/static/catregisterupload'
allowed_extensions = {'png','jpg', 'jpeg'}

def allowed_catfile(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

def convert_backslashes_to_forward_slashes(file_path):
    return file_path.replace('\\', '/')

@registercat.route('/register', methods=['GET', 'POST'])
def register_cat_form():
    cat_name = request.form['cat_name']
    cat_breed = ', '.join(request.form.getlist('cat_breed[]'))
    cat_age = request.form['cat_age']
    cat_gender = request.form['cat_gender']
    cat_neutered = request.form['cat_neutered']
    cat_vaccine = request.form['cat_vaccine']
    cat_special_needs = request.form['cat_special_needs']
    cat_about_me = request.form['cat_about_me']

    if 'cat_photo' in request.files: #to check if cat photo included in form
        catfile = request.files['cat_photo']

        if catfile.filename =='':
            flash('No selected file')
            return redirect(request.url)

        if catfile and allowed_catfile(catfile.filename): #check if the file is allowed
            filename = secure_filename(catfile.filename) #saving file
            file_path = os.path.join(upload_folder, filename)
            catfile.save(file_path)
            cat_photo = convert_backslashes_to_forward_slashes(file_path) #setting cat photo to saved file path
        else:
            flash('Invalid file format. Please upload an image file.')
            return redirect(request.url)

    else:
        cat_photo = None            

    formcat = RegisterCat(cat_name=cat_name,
                     cat_photo=cat_photo, 
                     cat_breed=cat_breed, 
                     cat_age=cat_age, 
                     cat_gender=cat_gender, 
                     cat_neutered=cat_neutered, 
                     cat_vaccine=cat_vaccine, 
                     cat_special_needs=cat_special_needs, 
                     cat_about_me=cat_about_me)

    db.session.add(formcat)
    db.session.commit()

    return redirect(url_for('views.profile_page'))

