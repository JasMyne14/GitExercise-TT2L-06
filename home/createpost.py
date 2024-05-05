from flask import Flask,Blueprint,render_template,redirect,request, url_for, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length
from .__init__ import *
from .models import Post
from flask_migrate import Migrate


createpost = Blueprint('createpost',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'peace'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

migrate = Migrate(app,db)


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

@createpost.route('/post/new', methods=['GET','POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Post creataed','success')
        return redirect(url_for('main'))
    return render_template('createpost.html', title='New Post')