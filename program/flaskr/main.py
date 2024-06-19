import re
import hashlib
import sqlite3
from flaskr import app
from flask import render_template, request, redirect, url_for, session

DATABASE = "login.db"

@app.route('/')
def index():
 return render_template(
  'index.html'
 )

@app.route('/add')
def add():
 return render_template(
  'add.html'
 )

@app.route('/check', methods=['POST', 'GET'])
def check():
 if request.method == 'POST':
  userID = request.form['userID']
  password1 = request.form['password1']
  password2 = request.form['password2']
  mail = request.form['mail']

  password_pattern = r'^(?=.*[0-9a-zA-Z\W]).{6,}$'
  mail_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

  con = sqlite3.connect(DATABASE)
  existing_user = con.execute("SELECT userID FROM user WHERE userID = ?", (userID,)).fetchone()
  existing_mail = con.execute("SELECT mail FROM user WHERE mail = ?", (mail,)).fetchone()
  con.close()

  if userID and password1 and password2 and mail and password1 == password2 and re.match(password_pattern, password1) and re.match(mail_pattern, mail) and not(existing_user) and not(existing_mail):
   
   user = {
    'userID' : userID,
    'password' : password1,
    'mail' : mail
   }

   session['user'] = user

   return render_template(
    'check.html',
    user=user
   )
  elif password1 != password2:
   error = "入力されたパスワードと確認用のパスワードが異なります"
  elif not(userID and password1 and password2 and mail):
   error = "全ての項目を入力してください"
  elif not(re.match(password_pattern, password1)):
   error = "パスワードは次の条件を満たしている必要があります。半角英数字記号を使用、6文字以上"
  elif not(re.match(mail_pattern, mail)):
   error = "正しいメールアドレスの形式ではありません。"
  elif existing_user:
   error = "ユーザーIDが既に存在します。別のユーザーIDを設定してください。"
  elif existing_mail:
   error = "このメールアドレスは既に登録されています。"
  # if文の外に記述すること
  return render_template(
   'add.html',
   error=error
  )
 
 else:
  return redirect(
   url_for('index')
  )
 
@app.route('/comp', methods=['POST', 'GET'])
def comp():
 if request.method == 'POST':
  user = session.get('user')

  hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()

  con = sqlite3.connect(DATABASE)
  con.execute("INSERT INTO user VALUES(?, ?, ?)", (user['userID'], hashed_password, user['mail']))
  con.commit()
  con.close()

  return render_template(
   'comp.html'
  )
 else:
  return redirect(
   url_for('index')
  )
 
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