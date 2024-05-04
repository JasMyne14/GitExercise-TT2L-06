from flask import Blueprint, render_template, request, redirect,url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from home import create_app
from .models import db,Post

views = Blueprint('views',__name__)

@views.route('/')
def main():
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
    return 'Post page'

@views.route('/adopt')
def adopt():
    return '<h2>Adoption page</h2>'
