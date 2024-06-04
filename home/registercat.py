from flask import Blueprint, request, redirect, url_for,flash, render_template
from .models import db, Cat
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os

registercat = Blueprint('registercat', __name__)

upload_folder = 'home/static/uploads'
allowed_extensions = {'png','jpg', 'jpeg'}


def allowed_catfile(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

@registercat.route('/register', methods=['GET', 'POST'])
def register_cat_form():
    if request.method == 'POST':
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
                flash('No selected file','danger')
                return redirect(request.url)

            if catfile and allowed_catfile(catfile.filename): #check if the file is allowed
                filename = secure_filename(catfile.filename) #saving file
                file_path = os.path.join(upload_folder, filename)
                catfile.save(file_path)
                cat_photo = url_for('static', filename=f'uploads/{filename}') #setting cat photo to saved file path
            else:
                flash('Invalid file format. Please upload an image file.', 'danger')
                return redirect(request.url)

        else:
            cat_photo = None            

        formcat = Cat(cat_name=cat_name,
                        cat_photo=cat_photo, 
                        cat_breed=cat_breed, 
                        cat_age=cat_age, 
                        cat_gender=cat_gender, 
                        cat_neutered=cat_neutered, 
                        cat_vaccine=cat_vaccine, 
                        cat_special_needs=cat_special_needs, 
                        cat_about_me=cat_about_me,
                        user_id = current_user.id)

        db.session.add(formcat)
        db.session.commit()

        flash('Cat registered successfully!', 'success')
        return redirect(url_for('views.catprofile'))

    return render_template('catregister.html')

@registercat.route('/edit/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def edit_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)

    if cat.user_id != current_user.id: # ensure the current user is the owner of the cat
        flash('You do not have permission to edit this cat.', 'danger')
        return redirect(url_for('views.catprofile'))

    if request.method == 'POST':
        cat.cat_name = request.form['cat_name']
        cat.cat_breed = ', '.join(request.form.getlist('cat_breed[]'))
        cat.cat_age = request.form['cat_age']
        cat.cat_gender = request.form['cat_gender']
        cat.cat_neutered = request.form['cat_neutered']
        cat.cat_vaccine = request.form['cat_vaccine']
        cat.cat_special_needs = request.form['cat_special_needs']
        cat.cat_about_me = request.form['cat_about_me']

        if 'cat_photo' in request.files:
            catfile = request.files['cat_photo']
            if catfile.filename != '' and allowed_catfile(catfile.filename):
                filename = secure_filename(catfile.filename)
                file_path = os.path.join(upload_folder, filename)
                catfile.save(file_path)
                cat.cat_photo = url_for('static', filename=f'uploads/{filename}')

        db.session.commit()
        flash(f'{cat.cat_name} updated successfully!', 'success')
        return redirect(url_for('views.catprofile'))

    return render_template('catedit.html', cat=cat)    

@registercat.route('/deletecat/<int:cat_id>', methods=['POST'])
@login_required
def delete_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)

    if cat.user_id != current_user.id:
        return redirect(url_for('views.catprofile'))

    db.session.delete(cat)
    db.session.commit()
    flash(f'{cat.cat_name} deleted successfully.', 'success')
    return redirect(url_for('views.catprofile'))    