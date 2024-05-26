from flask import Flask, Blueprint
from flask_socketio import SocketIO, emit
from .user_posts import *

notification = Blueprint('notification',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'notifications'
socketio = SocketIO(app)

# Sample data (replace with database integration)
users = {
    'user1': {'username': 'user1', 'notifications': []},
    'user2': {'username': 'user2', 'notifications': []}
}


@socketio.on('follow')
def handle_follow(data):
    follower = data['follower']
    followed = data['followed']
    message = f'{follower} started following you.'
    users[followed]['notifications'].append(message)
    emit('notification', {'message': message}, room=followed)

@socketio.on('like')
def handle_like(data):
    liker = data['liker']
    post_owner = data['post_owner']
    message = f'{liker} liked your post.'
    users[post_owner]['notifications'].append(message)
    emit('notification', {'message': message}, room=post_owner)

@socketio.on('comment')
def handle_comment(data):
    commenter = data['commenter']
    post_owner = data['post_owner']
    message = f'{commenter} commented on your post.'
    users[post_owner]['notifications'].append(message)
    emit('notification', {'message': message}, room=post_owner)

if __name__ == '__main__':
    socketio.run(app)
