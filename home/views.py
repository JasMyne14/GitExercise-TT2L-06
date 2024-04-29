from flask import Blueprint, render_template, request, send_from_directory


views = Blueprint('views',__name__)

@views.route('/')
def main():
    posts = [
        {'user': 'Aleez', 'title': 'First Post', 'content': 'Hello, this is my first post!'},
        {'user': 'Koyangi', 'title': 'Second Post', 'content': 'Another post here!'},
        {'user3': 'Jas', 'title': 'Third Post', 'content': 'Meow is meowing!'}
    ]
    return render_template('main.html', name='main', posts=posts)

@views.route('/notification')
def notification():
    users = {
        'user1': {'username': 'user1', 'notifications': []},
        'user2': {'username': 'user2', 'notifications': []}
    }    
    return render_template('notification.html', notification='Notification', users=users)

@views.route('/donation')
def donation():
    links= [{'url':"https://www.paws.org.my/donate", "text":"donate1"},
            {'url':"https://mnawf.org.my/donate/", "text":"donate2"},
            {'url':"https://catbeachpenang.com/donate/", "text":"donate3"}
    ]
    return render_template('donation.html', donation='donation', links=links)

@views.route('/post')
def post():
    return '<h1>Post page - make post</h1>'

@views.route('/adopt')
def adopt():
    return '<h2>Adoption page</h2>'