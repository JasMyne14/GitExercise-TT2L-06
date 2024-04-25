from flask import Blueprint, render_template, request


views = Blueprint('views',__name__)

@views.route('/')
def home():
    posts = [
        {'user': 'Aleez', 'title': 'First Post', 'content': 'Hello, this is my first post!'},
        {'user': 'Koyangi', 'title': 'Second Post', 'content': 'Another post here!'},
        {'user3': 'Jas', 'title': 'Third Post', 'content': 'Meow is meowing!'}
    ]
    return render_template('home.html', name='Home', posts=posts)

@views.route('/notification')
def notification():
    users = {
        'user1': {'username': 'user1', 'notifications': []},
        'user2': {'username': 'user2', 'notifications': []}
    }    
    return render_template('notification.html', notification='Notification', users=users)

@views.route('/about')
def about_us():
    print('About us page')
    return render_template('about_us.html', about='about')