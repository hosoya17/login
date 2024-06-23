import re
import hashlib
import sqlite3
from flaskr import app
from flask import render_template, request, redirect, url_for, session

from flaskr.routes.sing_up import sing_up
from flaskr.routes.sing_in import sing_in
from flaskr.routes.sing_out import sing_out

@app.route('/')
def index():
  return render_template(
    'index.html'
  )