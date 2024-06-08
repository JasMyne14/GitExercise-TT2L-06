from flask import Flask, Blueprint, render_template, request, redirect,url_for, flash, send_from_directory, session, abort, logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from home import create_app
from .forms import PostForm, SignUpForm, LoginForm, CommentForm
from .models import Post, User, Comment, Cat, Like, Notification, db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from .registercat import upload_folder, allowed_extensions
from werkzeug.utils import secure_filename
import os
from . import db
import secrets

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
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    return render_template('mainpage.html', mainpage='mainpage', user=current_user, posts=posts, profile_pic=profile_pic)

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
    notifications = Notification.query.filter_by(user_id=current_user.id, read=False).all()
    for notification in notifications:
        notification.read = True
    db.session.commit()
    current_user.recent_notification_count = 0
    db.session.commit()
    logout_user()
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('views.login'))

#@views.route('/like-noti/<int:post_id>')
#def like_noti(post_id):
    post = Post.query.get_or_404(post_id)
    notification = Notification(user_id=current_user.id, post_id=post_id, notification_type='like')
    db.session.add(notification)
    db.session.commit()
    return redirect(url_for('views.mainpage'))

#@views.route('/comment-noti/<int:post_id>')
#def comment_noti(post_id):
    post = Post.query.get_or_404(post_id)
    notification = Notification(user_id=current_user.id, post_id=post_id, notification_type='comment')
    db.session.add(notification)
    db.session.commit()
    return redirect(url_for('views.mainpage'))


#@views.route('/unread')
#def unread_noti(user_id):
    notification = Notification.query.filter_by(user_id=user_id, read=False).all()
    return render_template('notification.html', notifications=notification)

#@views.route('/read')
#def mark_as_read_noti(user_id):
    notifications = Notification.query.filter_by(user_id=user_id, read=False).all()
    for notification in notifications:
        notification.read = True
    db.session.commit()
    return redirect(url_for('views.display_noti'))

@views.route('/user_posts')
def user_posts():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    user_posts = Post.query.filter_by(author=current_user).all()
    return render_template('user_posts.html', posts=user_posts, profile_pic=profile_pic)

@views.route('/display/<filename>')
def display_image(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions

@views.route('/createpost', methods=['GET','POST'])
@login_required
def createpost():
    form = PostForm()
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    if form.validate_on_submit():
        file = form.file.data

        if file and display_image(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            file = url_for('static', filename=f'uploads/{filename}')
            flash('Your post has been created!','success')
        else:
            file = None
            flash('your post has been created (no file selected)','success')

        post = Post(title=form.title.data, content=form.content.data, author=current_user, file=file)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('views.mainpage'))
    return render_template('createpost.html', title='New Post', form=form, legend='New Post', profile_pic=profile_pic)

@views.route('/<int:post_id>')
def post(post_id):
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.all()

    return render_template('post.html', title=post.title, post=post, form=form, comments=comments, profile_pic=profile_pic)

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

        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated','success')
        return redirect(url_for('views.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.file.data = post.file
    return render_template('createpost.html', title='Update Post', form=form, legend='Update Post', profile_pic=profile_pic)

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

        if current_user != post.author:
            notification = Notification(user_id=current_user.id, post_id=post_id, notification_type='comment', comment_id=comment.id, like_id=None)
            db.session.add(notification)
            db.session.commit()
        return redirect(url_for('views.post', post_id=post_id))    
        
        return render_template('post.html', post=post, form=form, post_id=post_id, profile_pic=profile_pic)
    else:
        flash('Failed to add comment','error')
  
    return render_template('post.html', post=post, form=form, post_id=post_id, profile_pic=profile_pic, comment=comment)

@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

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

    return redirect(url_for('views.mainpage', profile_pic=profile_pic))

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

        if current_user != post.author:
            notification = Notification(user_id=post.author.id, post_id=post_id, notification_type='like', comment_id=None, like_id=like.id)
            db.session.add(notification)
            db.session.commit()
        return redirect(url_for('views.mainpage'))

    return redirect(url_for('views.mainpage'))

@views.route("/notification")
def display_noti():
    user_id = current_user.id
    notifications = Notification.query.filter(
        (exists().where((Post.id == Notification.post_id) & (Post.user_id == user_id))) &  
        ((Notification.notification_type == 'like') | (Notification.notification_type == 'comment'))).order_by(Notification.time.desc()).all()
    
    notification_count = len(notifications)

    comments = Comment.query.all()
    comment_ids = [n.comment_id for n in notifications if n.comment_id is not None]
    comments = Comment.query.filter(Comment.id.in_(comment_ids)).all()

    posts = Post.query.all()

    profile_pic= url_for('static', filename='default.jpg')
    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('notification.html', notifications=notifications, notification_count=notification_count, profile_pic=profile_pic, user_id=user_id, comments=comments, posts=posts)

@views.route('/donation')
def donation():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    links= [{'url':"https://www.paws.org.my/donate", "text":"donate1"},
            {'url':"https://mnawf.org.my/donate/", "text":"donate2"},
            {'url':"https://catbeachpenang.com/donate/", "text":"donate3"}
    ]
    return render_template('donation.html', donation='donation', links=links, profile_pic=profile_pic)

@views.route('/registercat')
def registercat():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    return render_template('catregister.html', profile_pic=profile_pic) 

@views.route('/catprofile')
def catprofile():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    formcat = Cat.query.all()
    return render_template('catprofile.html', formcat=formcat, profile_pic=profile_pic)

@views.route('/userprofile', methods=['GET'])
@login_required
def userprofile():
    form = User.query.all()
    profile_pic= url_for('static', filename='default.jpg')
    
    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    cats = Cat.query.filter(Cat.owner.has(id=current_user.id)).all()
    return render_template("userprofile.html", profile_pic=profile_pic, cats=cats)

@views.route('/user_edit', methods=['GET', 'POST'])
def user_edit():  
    user = User.query.get(current_user.id)
    form = SignUpForm(obj=user)
    profile_pic= url_for('static', filename='default.jpg')
    
    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            user.profile_pic = picture_file
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.username = form.username.data
        user.state = form.selected_option.data
        user.phonenumber = form.phonenumber.data
        db.session.commit()
        flash('Your profile has been updated !', 'success')
        return redirect(url_for('views.userprofile'))
    
    return render_template('user_edit.html', user=user, form=form, profile_pic=profile_pic)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn
   
@views.route('/adoptmeow')
@login_required
def adoptmeow():
    profile_pic= url_for('static', filename='default.jpg')

    if current_user.is_authenticated and current_user.profile_pic is not None:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    cats = db.session.query(Cat, User.state, User.email, User.phonenumber).join(User, Cat.user_id == User.id).filter(Cat.available_for_adoption == True).order_by(Cat.date_put_for_adoption.desc()).all()
    return render_template('adoptmeow.html', cats=cats, profile_pic=profile_pic)
    cats = db.session.query(Cat, User.state, User.email, User.phonenumber).join(User, Cat.user_id == User.id).filter(Cat.available_for_adoption == True).all()
    return render_template('adoptmeow.html', cats=cats)

@views.route('/profiledisplay<username>')
@login_required
def profiledisplay(username):
    user = User.query.filter_by(username=username).first_or_404()
    profile_pic = None

    if user.profile_pic:
        profile_pic = url_for('static', filename='profile_pics/' + user.profile_pic)

    cats = Cat.query.filter(Cat.owner.has(id=user.id)).all()

    return render_template('profiledisplay.html', user=user, profile_pic=profile_pic, cats=cats)
