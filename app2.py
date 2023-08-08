from scramble_generator import generate_scramble

import mysql.connector
from config import host, user, password, db_name
from flask import Flask, render_template, url_for, request, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

### configuration ###

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'database': 'scubertimer',
    'raise_on_warnings': True
}

app = Flask(__name__)
start_time = None
running = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/scubertimer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fgghaks92s2d5hfh32jkhh9hj38jdhs8hh35h8k2'


@app.route('/')
def hello():
    return render_template('new.html', scramble=generate_scramble())

@app.route('/generate_scramble', methods=['GET'])
def generate_scramble_route():
    new_scramble = generate_scramble()
    return new_scramble



# @app.route('/top')
# def top():
#     articles = Article.query.order_by(Article.date).all()
#     return render_template('top.html', articles=articles)


# @app.route('/settings')
# def settings():
#     articles = Article.query.order_by(Article.date).all()
#     return render_template('settings.html', articles=articles)


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         user = Article.query.filter_by(email=email).first()
#
#         if user and check_password_hash(user.password, password):
#             return render_template('profile.html', username=user.username, email=user.email)
#     return render_template('login.html')
#
#
# @app.route('/profile/<username>')
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return render_template('profile.html', username=username)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            cnx.close()
            return render_template('profile.html', username=user['username'], email=user['email'])

        cnx.close()
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def create_article():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        if request.form['password'] == request.form['password1']:
            password = generate_password_hash(request.form['password'])
        else:
            flash('Пароли не совпадают')

        try:
            query = "INSERT INTO users (username, email, password, date) VALUES (%s, %s, %s, %s)"
            data = (username, email, password, datetime.now())
            cursor.execute(query, data)
            cnx.commit()
            cnx.close()  # Вызов функции для вставки данных в базу
            flash('Вы успешно зарегистрировались')
        except:
            flash('Ошибка регистрации')


        return render_template('signup.html')  # Перенаправление на страницу входа

    return render_template('signup.html')


# @app.route('/signup', methods=['GET', 'POST'])
# def create_article():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'])
#         article = Article(username=username, email=email, password=password)
#
#         try:
#             db.session.add(article)
#             db.session.commit()
#             flash('Вы успешно зарегистрировались')
#         except:
#             flash('Ошибка регистрации')
#
#     return render_template('signup.html')



### ERRORS ###


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html'), 404


@app.errorhandler(401)
def unauthorized(error):
    return render_template('page401.html'), 401


if __name__ == '__main__':
    app.run(debug=True, port=5006)
