from flask import Blueprint, render_template

views = Blueprint('views',__name__)

@views.route('/')
def home():
    posts = [
        {'user': 'John', 'title': 'First Post', 'content': 'Hello, this is my first post!'},
        {'user': 'Jane', 'title': 'Second Post', 'content': 'Another post here!'},
        {'user3': 'Jas', 'title': 'Third Post', 'content': 'Meow is meowing!'}
    ]
    return render_template('home.html', name='Home', posts=posts)

@views.route('/notification')
def notification():
    return render_template('notification.html', name='Notification')