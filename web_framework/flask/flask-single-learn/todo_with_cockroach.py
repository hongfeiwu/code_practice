# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import abort
from flask import Response
from time import time
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_sqlalchemy import SQLAlchemy
import stub

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'cockroachdb://root@localhost:26257/bank?sslcert=certs/client.root.crt&sslkey=certs/client.root.key&sslmode=verify-full&sslrootcert=certs/ca.crt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_name = db.Column(db.String(80), unique=True)
    do_time = db.Column(db.String(120), unique=True)


@app.route('/todo')
def index():
    start = request.args.get('start', '')
    start = int(start) if start.isdigit() else 0
    todos = db.todos.find().sort([('created_at', -1)]).limit(10).skip(start)
    return dumps(todos)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
