# login

## 目次

- [login](#login)
  - [目次](#目次)
  - [実装内容](#実装内容)
      - [環境構築](#環境構築)
      - [Flaskアプリ起動](#flaskアプリ起動)
        - [Windows(CMD)環境](#windowscmd環境)
  - [プログラム解説](#プログラム解説)
    - [1. 前提](#1-前提)
    - [2. プログラム実行時に処理されるプログラム(対象ファイル：\_\_init\_\_.py)](#2-プログラム実行時に処理されるプログラム対象ファイル__init__py)
    - [3. プログラム実行時にindex.htmlを表示する(対象ファイル：main.py)](#3-プログラム実行時にindexhtmlを表示する対象ファイルmainpy)
    - [4. index.htmlからadd.html(新規登録画面)に遷移する(対象ファイル：main.py, index.html)](#4-indexhtmlからaddhtml新規登録画面に遷移する対象ファイルmainpy-indexhtml)
      - [main.py](#mainpy)
      - [index.html](#indexhtml)
    - [5. add.htmlのinput要素(テキストボックスなど)に入力された値を取得しcheck.html(確認画面)に表示する。(対象ファイル：main.py, add.html, check.html)](#5-addhtmlのinput要素テキストボックスなどに入力された値を取得しcheckhtml確認画面に表示する対象ファイルmainpy-addhtml-checkhtml)
      - [補足(POSTとGETの使い分けについて)](#補足postとgetの使い分けについて)
    - [6. セキュリティについて(対象ファイル：main.py, add.html, check.html)](#6-セキュリティについて対象ファイルmainpy-addhtml-checkhtml)
      - [GETで通信された場合](#getで通信された場合)
      - [やり方](#やり方)
        - [補足(render\_templateとredirectの違い)](#補足render_templateとredirectの違い)
      - [未入力チェック](#未入力チェック)
      - [やり方](#やり方-1)
      - [パスワード、メールアドレスの形式チェック](#パスワードメールアドレスの形式チェック)
      - [やり方](#やり方-2)
      - [パスワードの表示について](#パスワードの表示について)
      - [やり方](#やり方-3)
        - [補足](#補足)
    - [7. 入力されたデータをデータベースに保存する](#7-入力されたデータをデータベースに保存する)
      - [データベース作成](#データベース作成)
      - [db.py](#dbpy)
      - [\_\_init\_\_.py](#__init__py)
      - [補足(CREATE文の文法等々)](#補足create文の文法等々)
        - [主キーについて](#主キーについて)
        - [基本的な文法](#基本的な文法)
        - [NOT NULLについて](#not-nullについて)
        - [IF NOT EXISTSについて](#if-not-existsについて)

## 実装内容

- サインアップ機能<br>
- サインイン機能

#### 環境構築

事前にライブラリをインストールする必要がある。インストール方法は以下の通り。<br>

```Shell
pip install flask, jinja2, sqlite3
```

#### Flaskアプリ起動

Flaskアプリの起動方法は以下の通り。

##### Windows(CMD)環境

```Shell
set FLASK_APP=flaskr
set FLASK_ENV=development
set FLASK_DEBUG=1
flask run
```

## プログラム解説

### 1. 前提

以下のライブラリ、モジュールをインポートすること。htmlファイルなど必要なものは各自用意し、templatesフォルダに保存すること。

```diff_Python:main.py
import re
import hashlib
import sqlite3
from flaskr import app
from flask import render_template, request, redirect, url_for, session
```

### 2. プログラム実行時に処理されるプログラム(対象ファイル：\_\_init__.py)

```diff_Python:__init__.py
from flask import Flask
app = Flask(__name__)
import flaskr.main
```

### 3. プログラム実行時にindex.htmlを表示する(対象ファイル：main.py)

```diff_Python:main.py
@app.route('/')
def index():
    return render_template(
        'index.html'
    )
```

### 4. index.htmlからadd.html(新規登録画面)に遷移する(対象ファイル：main.py, index.html)

#### main.py

上記のindex関数とほとんど同じ。render_template関数は画面遷移する時に使用する。

```diff_Python:main.py
@app.route('/add')
def add():
    return render_template(
        'add.html'
    )
```

#### index.html

aタグのhref属性やformタグのaction属性に以下の様に記述する。{{}}を使えばhtmlにPythonのコードを埋め込めるようになる。

```diff_HTML:index.html
<!-- aタグの場合 -->
<a href="{{ url_for('add') }}">新規登録はこちら</a>
<!-- formタグの場合 -->
<form method="get" action="{{ url_for('add') }}>
  <input type="submit" value="新規登録">
</form>
```

### 5. add.htmlのinput要素(テキストボックスなど)に入力された値を取得しcheck.html(確認画面)に表示する。(対象ファイル：main.py, add.html, check.html)

- プログラムの通信方法はPOSTとする。<br>
- @app.routeの()内にmethods=['POST']と記述することにより、POSTでの通信が可能となる。<br>
- input要素に入力された値はrequest.form['name属性']で取得できる。<br>
- 遷移先の画面へ値を持っていくにはrender_template関数に変数名=値で持っていける。なお、分かりやすいように値は変数を参照し、変数名と値(変数を参照する場合)は同じ名前にすることをおすすめする。<br>
- 遷移先の画面(html)に値を表示するには{{}}内に変数名を記述することで表示できる。

```diff_Python:main.py
@app.route('/check', methods=['POST'])
def check():
  userID = request.form['userID']
  password1 = request.form['password1']
  password2 = request.form['password2']
  mail = request.form['mail']

  return render_template(
    'check.html',
    userID=userID,
    password1=password1,
    mail=mail
  )
```

```diff_HTML:add.html
<!-- 以下の様に必ずname属性を記述すること。以下のコードの記述場所はどこでも良い -->
<form method="post" action="{{ url_for('check') }}">
  <input type="text" name="userID">
  <input type="password" name="password1">
  <input type="password" name="password2">
  <input type="text" name="mail">
  <input type="submit" value="確認">
</form>
```

```diff_HTML:check.html
<!-- 以下はpタグで表示しているが、文字が表示できるタグであれば何でも良い -->
<p>{{ userID }}</p>
<p>{{ password1 }}</p>
<p>{{ mail }}</p>
```

#### 補足(POSTとGETの使い分けについて)

input要素で入力された値を取得、保存する時の通信方法はPOST、そうでない時(画面遷移など)はGETと覚えておく程度で良い。<br>
もう少し詳しくPOSTとGETの違いについて知りたい場合はググるかIパスやFEなどの参考書を参照すると良い。

### 6. セキュリティについて(対象ファイル：main.py, add.html, check.html)

#### GETで通信された場合

現状、ブラウザのurl欄にcheck.htmlのurl(localhost:5000/check)を入力するとエラーが表示される。<br>
実際にクラッカーなどはこのエラーメッセージを読み攻撃手法を考えるらしいので、表示されないようにする。

#### やり方

- url欄に直接urlを入力してアクセスすると、通信方法はGETになる為、通信方法がGETの場合index.htmlなどにリダイレクトしてやれば良い。
- @app.routeのmethods=['POST']に'GET'を追加する。
- request.methodで通信方法を取得できるので、if文でPOSTでの通信の処理と、GETでの通信の処理を分けてやれば良い。
- リダイレクトはredirect関数とurl_for関数を使う。html内でも出てきたが、url_for関数は拡張子(.html)は不要である。

##### 補足(render_templateとredirectの違い)

実際に試してみると分かるが、render_templateは表示されているhtmlが同じものであろうと、urlには処理された関数名が表示される。<br>
redirectはurl_for関数に記述してある関数を実行する為、リダイレクト先の関数名が表示される。

```diff_Python:main.py
@app.route('/check', methods=['POST', 'GET']) # 敢えて、GETでの通信も許可してやる。
def check():
 + if request.method == 'POST':
    userID = request.form['userID']
    # 以下略
 + else:
  + return redirect(
   + url_for('index')
  + )
```

#### 未入力チェック

現状、何も入力していなくてもcheck.htmlに遷移してしまう。<br>
空のデータがデータベースに保存されてしまうのはまずいので、何とかする。<br>
入力されていないデータがある場合はadd.htmlに遷移し、エラーを表示するようにする。

#### やり方

- if文で変数に何も値が入っていないものを区別すれば良い。
- なぜ下記の条件式でできるのか分からない人は、Python falsyで検索すること。

```diff_Python:main.py
mail = request.form['mail']
+ if userID and password1 and password2 and mail:
    return render_template(
        'check.html',
        userID=userID,
        password1=password1,
        mail=mail
    )
+ else:
    + erro = "全ての項目を入力してください"
    + return render_template(
        + 'add.html',
        + error=error
    + )
    # 以下略
```

```diff_HTML:add.html
{% if error %}
    <p>{{ error }}</p>
{% endif %}
<form method="post" action="{{ url_for('check') }}">
  <input type="text" name="userID">
  <!-- 以下略 -->
```

#### パスワード、メールアドレスの形式チェック

現状、パスワードとメールアドレスは何を入力してもcheck.htmlに遷移してしまう。<br>
パスワードに関しては、強度の高いパスワードを設定させるようにするのが望ましい。<br>
強度が低いパスワードを入力されたらエラーを表示するようにする。<br>
確認用で同じパスワードを入力させ比較し、違うものが入力されていたらエラーを表示するようにする。<br>
メールアドレスに関しては正しい形式でなければエラーを表示するようにする。

#### やり方

- if文で正規表現と比較する。
- 以下パスワードは6文字以上半角英数字記号を使用できるようにしたものである。<br>
※if文の条件式が長い為、横までスクロールして確認すること。

```diff_Python:main.py
mail = request.form['mail']

password_pattern = r'^(?=.*[0-9a-zA-Z\W]).{6,}$'
mail_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
+ if userID and password1 and password2 and mail and password1 == password2 and re.match(password_pattern, password1) and re.match(mail_pattern, mail):
    # 省略
+ elif password1 != password2:
    error = "入力されたパスワードと確認用のパスワードが異なります"
+ elif not(userID and password1 and password2 and mail):
    error = "全ての項目を入力してください"
+ elif not(re.match(password_pattern, password1))
    + error = "パスワードは次の条件を満たしている必要があります。半角英数字記号を使用、6文字以上"
+ elif not(re.match(mail_pattern, mail))
    + error = "正しいメールアドレスの形式ではありません。"
# if文の外に記述すること
return render_template(
    'add.html',
    error=error
    )
# 以下略
```

#### パスワードの表示について

現状、画面遷移先で入力されたパスワードが表示される。<br>
セキュリティ的に良くないので●などで伏せて表示されるようにする。

#### やり方

- check.htmlにて乗算やlengthを使用し、パスワードの文字数分●を表示するようにする。

```diff_HTML:check.html
<p>{{ userID }}</p>
+ <p>{{ '●' * user.password|length }}</p>
<p>{{ mail }}</p>
```

##### 補足

このやり方もパスワードの文字数が分かってしまう為、万全なセキュリティ対策とは言えない。<br>
もしこれよりもセキュリティを万全にしたい場合は各自で調べること。

### 7. 入力されたデータをデータベースに保存する

データベースはSQLite3を使用する。

#### データベース作成

ユーザーテーブルを作成する。テーブル定義は以下の通り。

|No.|カラム名|データ型|Not Null|デフォルト|備考|
|----|----|----|----|----|----|
|1|userID|VARCHAR|NOT NULL||ユーザーのID|
|2|hashed_password|VARCHAR|NOT NULL||ユーザーのハッシュ化されたパスワード|
|3|mail|VARCHAR|NOT NULL||ユーザーのメールアドレス|

#### db.py

- db.pyではテーブルの作成を行う。つまり、CREATE文しか記述しない。
- `con = sqlite3.connect(DATABASE)`でデータベースと接続できる。
- `con.execute("")`の""の中にSQL文を記述する。なお、''でも動作するが、SQLの文法上''を使用することが多々ある為、""を使用することをおすすめする。
- `con.close()`でデータベースとの接続を切断できる。用事が済んだら必ず切断すること。

```diff_Python:db.py
import sqlite3

DATABASE = 'データベース名.db'

def create_expenses_table():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS user(userID VARCHAR PRIMARY KEY, hashed_password VARCHAR NOT NULL, mail VARCHAR NOT NULL)")
    con.close()
```

#### \_\_init__.py

以下を追記して、実行時にデータベースが作成されるようにする。

```diff_Python:__init__.py
from flaskr import db
db.create_expenses_table()
```

#### 補足(CREATE文の文法等々)

##### 主キーについて

- PRIMARY KEYと記述する。
- 重複を許さない。
- NULL(空文字)を許さない。
- 基本的に一番最初に記述する。

##### 基本的な文法

```diff_SQL
CREATE TABLE テーブル名(カラム名1 型名 PRIMARY KEY, カラム名2 型名)
```

##### NOT NULLについて

主キー以外でNULLを許さない場合、NOT NULLと記述する。

```diff_SQL
CREATE TABLE テーブル名(カラム名 型名 主キー, カラム名 型名 NOTNULL)
```

##### IF NOT EXISTSについて

PythonやPHPなどのプログラミング言語でデータベースを作成するプログラムを記述すると、毎回CREATE文が実行されてしまう。<br>
2度目の実行は不要な上に、データが全て消えてしまう危険性がある為、テーブルが存在しない時だけCREATE文を実行するようにしたい。<br>
IF NOT EXISTSを使用すれば上記のことが解決できる。

```diff_SQL
CREATE TABLE IF NOT EXISTS テーブル名(カラム名 型名 主キー, カラム名 型名 NOTNULL)
```