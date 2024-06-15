from flask import Flask, Blueprint, render_template, request, redirect,url_for, flash, send_from_directory, session, abort, logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists, desc
from home import create_app
from .forms import PostForm, SignUpForm, LoginForm, CommentForm, UpdateProfileForm
from .models import Post, User, Comment, Cat, Like, Notification, AdoptionNotification, db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .registercat import upload_folder, allowed_extensions
from werkzeug.utils import secure_filename
import os
from .adoptmeow import adoptmeow
import secrets
import pytz
from pytz import timezone
from datetime import datetime

views = Blueprint('views',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'appviews'
app.config['upload_folder'] = upload_folder
app.config['TIMEZONE'] = 'Asia/Kuala_Lumpur'

# First Page
@views.route('/')
def first():
    session.clear()
    return render_template('firstpage.html', name='firstpage')

# Mainpage
@views.route('/mainpage')
def mainpage():
    posts = Post.query.order_by(Post.date.desc()).all()
    comments = Comment.query.all()
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    # To convert the timezone for each post's date
    for post in posts:
        post.date = convert_timezone(post.date)
    return render_template('mainpage.html', mainpage='mainpage', user=current_user, posts=posts, profile_pic=profile_pic, comments=comments)

#Sign Up Page
@views.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()

    # To check if the form is submitted and validated
    if form.validate_on_submit():

        # To generate a hashed password from the form data
        hashed_password = generate_password_hash(form.password1.data)

        # To create new User with the form data
        user = User(fullname=form.fullname.data,
                    email=form.email.data,
                    username=form.username.data,
                    password1=hashed_password,
                    password2=hashed_password,
                    state=form.selected_option.data,
                    phonenumber=form.phonenumber.data)
        
        # To add the new user to the database session
        db.session.add(user)

        # To commit the session to save the new user to the database
        db.session.commit()

        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('views.login'))
    return render_template('signup.html', form=form)

#Login Page
@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.mainpage'))
    
    form = LoginForm()

    # To check if the form is submitted and validated
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # To verify the user's password
        if user and check_password_hash(user.password1, form.password1.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('views.mainpage'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
            return redirect(url_for('views.login'))
    return render_template('login.html', form=form)

# Log Out Page
@views.route('/logout')
def logout():

    notifications = Notification.query.filter_by(user_id=current_user.id, read=False).all()
    for notification in notifications:
        notification.read = True
    current_user.unread_notification_count = 0

    # To commit changes to the database
    db.session.commit()

    #Log the user out
    logout_user()

    # To clear the session data
    session.clear()
    flash('Logged out successfully!', 'success')

    return redirect(url_for('views.login'))

# User Post 
@views.route('/user_posts')
def user_posts():
    profile_pic= url_for('static', filename='default.jpg')

    # display profile picture
    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    # display user's post
    user_posts = Post.query.filter_by(author=current_user).all()
    return render_template('user_posts.html', posts=user_posts, profile_pic=profile_pic)

# allow image to be displayed on each page
@views.route('/display/<filename>')
def display_image(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Create Post Page
@views.route('/createpost', methods=['GET','POST'])
@login_required
def createpost():
    form = PostForm()
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    if form.validate_on_submit():
        file = form.file.data

        #save image at upload folder
        if file and display_image(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            file = url_for('static', filename=f'uploads/{filename}')
            flash('Your post has been created!','success')
        else: #post without image
            file = None
            flash('your post has been created (no file selected)','success')

        #insert to database
        post = Post(title=form.title.data, content=form.content.data, author=current_user, file=file)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('views.mainpage'))
    return render_template('createpost.html', title='New Post', form=form, legend='New Post', profile_pic=profile_pic)

#display specific post based on post id
@views.route('/<int:post_id>')
def post(post_id):
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.all()

    return render_template('post.html', title=post.title, post=post, form=form, comments=comments, profile_pic=profile_pic)

# update post function
@views.route('/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

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

        # add new edited post to database
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated','success')
        return redirect(url_for('views.post', post_id=post.id))
    
    #get previous data from database
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.file.data = post.file
    return render_template('createpost.html', title='Update Post', form=form, legend='Update Post', profile_pic=profile_pic)

# delete post function
@views.route('/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    post = Post.query.get_or_404(post_id)
    comment = Comment.query.first()

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.delete(comment)
    db.session.commit()
    flash('Post has been deleted','success')
    return redirect(url_for('views.mainpage', profile_pic=profile_pic))

#create comment function for each specific post
@views.route('/create-comment/<int:post_id>', methods=['GET','POST'])
@login_required
def create_comment(post_id):
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    #comment = Comment.query.get_or_404(post_id)

    if form.validate_on_submit():
        comment = Comment(text=form.text.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!','success')
        form.text.data = ""

        #add comment notifications to database
        if current_user != post.author:
            notification = Notification(user_id=current_user.id, post_id=post_id, notification_type='comment', comment_id=comment.id, like_id=None)
            db.session.add(notification)
            db.session.commit()

            #count unread notifications
            owner = User.query.get(post.author.id)
            owner.unread_notification_count +=1

            db.session.commit()
            return redirect(url_for('views.post', post_id=post_id))    
        return render_template('post.html', post=post, form=form, post_id=post_id, profile_pic=profile_pic)

    else:
        flash('Failed to add comment','error')
  
    return render_template('post.html', post=post, form=form, post_id=post_id, profile_pic=profile_pic, comment=comment)

# delete comment function
@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    form = CommentForm()
    comment = Comment.query.filter_by(id=comment_id).first()

    #if comment noneexisted
    if not comment:
        flash('Comment does not exists','error')

    #if current user is not the author or the post's owner
    elif current_user != comment.author and current_user != comment.post.author:
        flash('Permission denied','error')

    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted','success')

    return redirect(url_for('views.mainpage', profile_pic=profile_pic))

# like-post function
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

        # add and count unread notifications
        if current_user != post.author:
            notification = Notification(user_id=post.author.id, post_id=post_id, notification_type='like', comment_id=None, like_id=like.id)
            db.session.add(notification)
            db.session.commit()

        owner = User.query.get(post.author.id)
        owner.unread_notification_count +=1

        db.session.commit()
        return redirect(url_for('views.mainpage'))

    return redirect(url_for('views.mainpage'))

# notification settings
@views.route("/notification")
@login_required
def display_noti():
    user_id = current_user.id
    notifications = [] #gather notifications as a list
    # get notifications from database for specific user
    like_comment_notifications = Notification.query.filter(
        (exists().where((Post.id == Notification.post_id) & (Post.user_id == user_id))) &  
        ((Notification.notification_type == 'like') | (Notification.notification_type == 'comment'))).order_by(Notification.date.desc()).all()
    notifications.extend(like_comment_notifications)

    # get adoption notification from database
    adoption_notifications = AdoptionNotification.query.filter_by(user_id=user_id).all()
    notifications.extend(adoption_notifications)
    #display notification according to date (newest)
    notifications.sort(key=lambda x: x.date, reverse=True)

    # convert date to localtime zone
    for notification in notifications:
        utc_timestamp = notification.date
        local_timezone = pytz.timezone(app.config['TIMEZONE'])
        local_timestamp = utc_timestamp.astimezone(local_timezone)
        notification.date = local_timestamp

        # mark unread noti as read
        if not notification.read:
            notification.read=True
    db.session.commit()

    # get comment notification for user
    comment_ids = [n.comment_id for n in notifications if hasattr(n, 'comment_id') and n.comment_id is not None]
    comments = Comment.query.filter(Comment.id.in_(comment_ids)).all()

    #get post associated with the notifications
    post_ids = [n.post_id for n in notifications if hasattr(n, 'post_id') and n.post_id is not None]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    #posts = Post.query.all()

    profile_pic= url_for('static', filename='default.jpg')
    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    
    # count total unread notifications
    unread_notification_count = sum(1 for notification in notifications if not notification.read)

    # get cat data from database
    cats = {}
    for notification in adoption_notifications:
        cat = Cat.query.get(notification.cat_id)
        if cat:
            cats[notification.id] = cat

    #get adopter data from database
    adopter_names = {}
    for notification in adoption_notifications:
        adopter = User.query.get(notification.adopter_id)
        if adopter:
            adopter_names[notification.id] = adopter.fullname

    return render_template('notification.html', notifications=notifications, unread_notification_count=unread_notification_count, profile_pic=profile_pic, user_id=user_id, comments=comments, posts=posts, cats=cats, adopter_names=adopter_names)

# Donation Page 
@views.route('/donation')
def donation():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    return render_template('donation.html', profile_pic=profile_pic)

#Registration Cat Page
@views.route('/registercat')
def registercat():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    return render_template('catregister.html', profile_pic=profile_pic) 

# Cat Profile Page
@views.route('/catprofile')
def catprofile():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    formcat = Cat.query.all()
    return render_template('catprofile.html', formcat=formcat, profile_pic=profile_pic)

# User Profile Page
@views.route('/userprofile', methods=['GET'])
@login_required
def userprofile():
    form = User.query.all()
    profile_pic= url_for('static', filename='default.jpg')
    
    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    # Queries the database for all cats owned by the current_user
    cats = Cat.query.filter(Cat.owner.has(id=current_user.id)).all()
    return render_template("userprofile.html", profile_pic=profile_pic, cats=cats)

# Update User Page
@views.route('/user_edit', methods=['GET', 'POST'])
def user_edit():  
    user = User.query.get(current_user.id)
    form = UpdateProfileForm(obj=user)
    profile_pic = url_for('static', filename='default.jpg')
    
    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    #To handle form submission from the update user page
    if form.validate_on_submit():

        # If a new profile picture is uploaded, save it and updated it
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            user.profile_pic = picture_file
        
        # To update the user's details with the form data
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.username = form.username.data
        user.state = form.selected_option.data
        user.phonenumber = form.phonenumber.data

        # To commit the changes to the database
        db.session.commit()

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('views.userprofile'))
    
    return render_template('user_edit.html', user=user, form=form, profile_pic=profile_pic)

def save_picture(form_picture):

    # To secure the filename provided by user
    filename = secure_filename(form_picture.filename)

    #To construct the full path where the picture will be saved
    picture_path = os.path.join(app.root_path, 'static/profile_pics', filename)

    # To check if the directory where the picture will be saved exists
    if not os.path.exists(os.path.dirname(picture_path)):
        os.makedirs(os.path.dirname(picture_path))

    # To ensure the filename is unique by adding a random hex if the file already exists
    while os.path.exists(picture_path):

        random_hex = secrets.token_hex(4)
        filename = f"{os.path.splitext(filename)[0]}_{random_hex}{os.path.splitext(filename)[1]}"
        picture_path = os.path.join(app.root_path, 'static/profile_pics', filename)
    
    # Save the picture to the defined path
    form_picture.save(picture_path)
    
    return filename   

views.register_blueprint(adoptmeow)   
@views.route('/adoptmeow')
@login_required
def adoptmeow():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    cats = db.session.query(Cat, User.state, User.email, User.phonenumber).join(User, Cat.user_id == User.id).filter(Cat.available_for_adoption == True).order_by(Cat.date_put_for_adoption.desc()).all()
    return render_template('adoptmeow.html', cats=cats, profile_pic=profile_pic)

# Profile Display Page
@views.route('/profiledisplay/<username>')
@login_required
def profiledisplay(username):

    # To find the the user by username from the User table
    user = User.query.filter_by(username=username).first_or_404()
    profile_pic = url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    
    # Queries the database for all cats owned by the user
    cats = Cat.query.filter(Cat.owner.has(id=user.id)).all()

    # Queries the database for the first post authored by the user
    post = Post.query.filter_by(author=user).first()

    return render_template('profiledisplay.html', user=user, profile_pic=profile_pic, cats=cats, post=post)

def convert_timezone(utc_timestamp):
    local_timezone = pytz.timezone(app.config['TIMEZONE'])
    return utc_timestamp.astimezone(local_timezone)

# Other's User Post
@views.route('/otheruser_post/<username>')
def otheruser_post(username):
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    # To find the the user by username from the User table
    user = User.query.filter_by(username=username).first_or_404()
    # Create a comment form
    form = CommentForm()
    # Get all the posts that authored by user
    posts = Post.query.filter_by(author=user).order_by(desc(Post.date)).all()  
    # Get all the comment from the database  
    comments = Comment.query.all()

    return render_template('otheruser_post.html', posts=posts, form=form, comments=comments, profile_pic=profile_pic, user=user)
