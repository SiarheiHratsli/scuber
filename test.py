#!/usr/bin/env /Applications/MAMP/Library/bin/python

import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
    'database': 'scubertimer',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor(dictionary=True)

cursor.execute('SELECT * FROM `users`')

results = cursor.fetchall()

for row in results:
    user_id = row['id']
    username = row['username']
    email = row['email']
    password = row['password']
    age = row['age']
    date = row['date']
    print(f'ID: {user_id}, Username: {username}, email: {email}, password: {password}, age: {age}, date: {date}')

cnx.close()
