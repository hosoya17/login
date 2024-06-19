@echo off
@REM ディレクトリ変更忘れずに
cd \python\program
set FLASK_APP=flaskr
set FLASK_ENV=development
set FLASK_DEBUG=1
python -m flask run