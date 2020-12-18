from flask import Flask
from flask import url_for
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route('/table/<sex>/<int:age>')
def table(sex, age):
    return"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Миссия колонизация Марса</title>
                  </head>
                  <body>
                    <h1>Миссия колонизация Марса</h1>
                    <p1>И на Марсе будут яблони цвести!</p1>
                  </body>
                </html>""" # format(sex, str(type(username))[1:-1], number, str(type(number))[1:-1])
#

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')