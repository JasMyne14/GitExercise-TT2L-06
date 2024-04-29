from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask('__name__')
app.secret_key = 'new-account'

#MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'flask_users'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login (): 
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = msql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_users WHERE username = % s AND password = % s', (username, password))
        user = cursor.fetchnone()
        if user: 
            session['loggedin']= True
            session['id'] = user['id']
            session['full_name'] = user['full_name']
            session['email'] = user['email']
            mesage = 'Logged in succesfully !'
            return render_template('login.html')
        else:
            mesage = ''


@app.route('/')
def logout():
    session.pop('loggedin', None)
    session.pop('loggedin', None)
    session.pop('loggedin', None) 
    return redirect(url_for('login'))

@app.route('/register', methods =['GET','POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQL.dbcursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_users WHERE email = % s', (email, ))
        account = cursor.fetchnone()
        if account:
            mesage = 'Account Already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not username or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO tbl_users VALUES (NULL, % s, & s,% s)', (username, email, password, ))
            mysql.connection.commit()
            mesage ='You have succesfully registered ! '
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html')

if __name__ == "__main__" :
    app.run(debug=True)
