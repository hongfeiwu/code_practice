# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.script import Manager
from raven.contrib.flask import Sentry
import logging
from flask import request

app = Flask(__name__)
# sentry = Sentry(app, dsn='http://d202ee7ccbea457c8c3707dbe495c978:4e18c5a3693b493fb149723f671dc2ca@sentry.whf.com/2')


@app.route('/')
def index():
    username = request.cookies.get('username')
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello Woaaarld'


@app.route('/user/<username>', methods=['GET', 'POST'])
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')


if __name__ == '__main__':
    # __main__ 当前程序启动运行的模块名
    # __name__ 当前模块的模块名
    app.debug = True
    app.run(host='0.0.0.0')


