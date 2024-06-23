@echo off
cd \python\login\ファイル分割後
set FLASK_APP=flaskr
set FLASK_ENV=development
set FLASK_DEBUG=1
python -m flask run