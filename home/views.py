from flask import Flask, Blueprint, render_template, request, redirect,url_for, flash, send_from_directory, session,session, abort
from flask_sqlalchemy import SQLAlchemy
from home import create_app
from .forms import PostForm, SignUpForm, LoginForm, CommentForm
from .models import Post, User, Comment, Cat, Like, db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .registercat import upload_folder, allowed_extensions
from werkzeug.utils import secure_filename
import os
from . import db

views = Blueprint('views',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'appviews'
app.config['upload_folder'] = upload_folder


@views.route('/')
def first():
    return render_template('firstpage.html', name='firstpage')

@views.route('/mainpage')
def mainpage():
    posts = Post.query.order_by(Post.date.desc()).all()
    comments = Comment.query.all()
    return render_template('mainpage.html', mainpage='mainpage', user=current_user, posts=posts)

@views.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password1.data)
        user = User(fullname=form.fullname.data,
                    email=form.email.data,
                    username=form.username.data,
                    password1=hashed_password,
                    password2=hashed_password,
                    state=form.selected_option.data,
                    phonenumber=form.phonenumber.data)
        db.session.add(user)
        db.session.commit()
        selected_option = form.selected_option.data
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('views.login'))
    return render_template('signup.html', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.mainpage'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password1, form.password1.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('views.mainpage'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
            return redirect(url_for('views.login'))
    return render_template('login.html', form=form)

@views.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('views.login'))

@views.route('/notification')
def notification():
    users = {
        'user1': {'username': 'user1', 'notifications': []},
        'user2': {'username': 'user2', 'notifications': []}
    }    
    return render_template('notification.html', notification='Notification', users=users) 

@views.route('/user_posts')
def user_posts():
    user_posts = Post.query.filter_by(author=current_user).all()
    return render_template('user_posts.html', posts=user_posts)

@views.route('/display/<filename>')
def display_image(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

@views.route('/createpost', methods=['GET','POST'])
@login_required
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        file = form.file.data

        if file and display_image(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            file = url_for('static', filename=f'uploads/{filename}')
            flash('Your post has been created!','success')
        else:
            file_photo = None
            flash('your post has been created (no file selected)','success')

        post = Post(title=form.title.data, content=form.content.data, author=current_user, file=file_photo)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('views.mainpage'))
    return render_template('createpost.html', title='New Post', form=form, legend='New Post')

@views.route('/<int:post_id>')
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.all()
    return render_template('post.html', title=post.title, post=post, form=form, comments=comments)

@views.route('/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        file = form.file.data 
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            file = url_for('static', filename=f'uploads/{filename}')

        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated','success')
        return redirect(url_for('views.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.file.data = post.file
    return render_template('createpost.html', title='Update Post', form=form, legend='Update Post')

@views.route('/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.first()

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.delete(comment)
    db.session.commit()
    flash('Post has been deleted','success')
    return redirect(url_for('views.mainpage'))

@views.route('/create-comment/<int:post_id>', methods=['GET','POST'])
@login_required
def create_comment(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!','success')
        form.text.data = ""
        return render_template('post.html', post=post, form=form, post_id=post_id)
    else:
        flash('Failed to add comment','error')
    return redirect(url_for('views.mainpage', post_id=post_id))

@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    form = CommentForm()

    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exists','error')

    elif current_user != comment.author and current_user != comment.post.author:
        flash('Permission denied','error')

    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted','success')

    return redirect(url_for('views.mainpage'))

@views.route('/like-post/<int:post_id>',methods=['GET','POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(author=current_user, post_id=post_id).first()

    if not post:
        flash('Post does not exists','error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('views.mainpage'))

@views.route('/donation')
def donation():
    links= [{'url':"https://www.paws.org.my/donate", "text":"donate1"},
            {'url':"https://mnawf.org.my/donate/", "text":"donate2"},
            {'url':"https://catbeachpenang.com/donate/", "text":"donate3"}
    ]
    return render_template('donation.html', donation='donation', links=links)

@views.route('/registercat')
def registercat():
    return render_template('catregister.html') 

@views.route('/profile_page')
def profile_page():
    formcat = Cat.query.all()
    return render_template('catprofile.html', formcat=formcat)

@views.route('/userprofile', methods=['GET','POST'])
def userprofile():
    form = User.query.all()
    return render_template("userprofile.html")

@views.route('/user_edit', methods=['GET', 'POST'])
def user_edit():  
    user = User.query.get(current_user.id)
    form = SignUpForm(obj=user)

    if form.validate_on_submit():
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.username = form.username.data
        user.state = form.selected_option.data
        user.phonenumber = form.phonenumber.data
        db.session.commit()
        flash('Your profile has been updated !', 'success')
        return redirect(url_for('views.userprofile'))
    
    return render_template('user_edit.html', user=user, form=form)

   
@views.route('/adoptmeow')
def adoptmeow():
    return render_template('adoptmeow.html')