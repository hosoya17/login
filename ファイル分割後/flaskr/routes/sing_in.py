import re
import hashlib
import sqlite3
from flaskr import app
from flask import render_template, request, redirect, url_for, session

def sing_in(app):
    @app.route('/top', methods=['GET', 'POST'])
    def top():
        if request.method == 'POST':
            userID = request.form['userID']
            hashed_password = hashlib.sha256(request.form['password'].encode()).hexdigest()

            con = sqlite3.connect(DATABASE)
            existing = con.execute("SELECT * FROM user WHERE userID = ? AND hashed_password = ?", (userID, hashed_password)).fetchall()
            con.close()

            if existing:
                session['userID'] = userID
                return render_template(
                    'top.html',
                    userID=userID
                )
            else:
                error = 'ユーザーIDかパスワードが間違っています。'
                return render_template(
                    'index.html',
                    error=error
                )
        else:
            if 'userID' in session:
                userID = session['userID']

                return render_template(
                    'top.html',
                    userID=userID
                )
            else:
                error = '長時間操作が行われなかったため、ログアウトしました。'
                return render_template(
                    'index.html',
                    error=error
                )
