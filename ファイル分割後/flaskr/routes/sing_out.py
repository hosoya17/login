import hashlib
from flaskr import app
from flask import redirect, url_for, session

def sing_out(app):
    @app.route('/logout')
    def logout():
        session.pop('userID', None)
        return redirect(
            url_for('index')
        )