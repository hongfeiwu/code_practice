# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import abort
from flask import Response
from time import time
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo

app = Flask(__name__)

mongo = pymongo.MongoClient('127.0.0.1', 27017)
db = mongo.todo


class Todo(object):
    @classmethod
    def create_doc(self, content):
        return {
            'content': content,
            'created_at': time(),
            'is_finished': False,
            'finished_at': None
        }


@app.route('/todo')
def index():
    start = request.args.get('start', '')
    start = int(start) if start.isdigit() else 0
    todos = db.todos.find().sort([('created_at', -1)]).limit(10).skip(start)
    return dumps(todos)


@app.route('/todo', methods=['POST'])
def add():
    content = request.form.get('content', None)
    if not content:
        abort(400)
    db.todos.insert(Todo.create_doc(content))
    return Response()    # 200


@app.route('/todo/<tid>/finish', methods=['PUT'])
def finish(tid):
    result = db.todos.update_one(
        {'_id': ObjectId(tid)},
        {
            '$set': {
                'is_finished': True,
                'finished_at': time()
            }
        }
    )
    if result.matched_count == 0:
        abort(404)
    return Response()


@app.route('/todo/<tid>', methods=['DELETE'])
def delete(tid):
    result = db.todos.delete_one(
        {'_id': ObjectId(tid)}
    )
    if result.matched_count == 0:
        abort(404)
    return Response()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
