from flask import Flask,Blueprint,render_template,redirect,request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from .__init__ import *
from home import create_app

post = Blueprint('post',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'love'


@post.route('/add_post', methods=['POST'])
def add_post():
    data = request.json
    return jsonify({'message':'Post added successfully'})

@post.route('/edit_post/<int:post_id>', methods=['PUT'])
def edit_post(post_id):
    data = request.json  # Assuming JSON data is sent
    # Add code to edit post in the database
    return jsonify({'message': 'Post edited successfully'})

@post.route('/delete_post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Add code to delete post from the database
    return jsonify({'message': 'Post deleted successfully'})

@post.route('/add_post',methods=['GET'])
def add_post_page():
    return render_template('post.html')