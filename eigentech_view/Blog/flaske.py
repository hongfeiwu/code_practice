# coding=utf-8
from flask import Flask, request, abort, redirect, url_for
import user
import article

app = Flask(__name__)

app.register_blueprint(user.bp)
app.register_blueprint(article.bp)

app.config.from_object('config')  # 通过字符串的模块名字加载


@app.route('/',endpoint="good")
def index():
    return "Good jod"


@app.route('/<int:ids>',endpoint="bad")
def index(ids):
    return "%s" % ids


@app.route('/people/')
def people():
    name = request.args.get('name')
    if not name:
        return redirect(url_for('login'))
    user_agent = request.headers.get('User-Agent')
    return 'Name: {0}; UA: {1}'.format(name, user_agent)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.headers.get('user_id')
        return 'User: {} login'.format(user_id)
    else:
        return 'Open Login page'


@app.route('/secret/')
def secret():
    abort(401)
    print 'This is never executed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=app.debug)
