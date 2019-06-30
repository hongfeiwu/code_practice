# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from functools import wraps
from flask import request, session, g, redirect, url_for, abort, flash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False, index=True)
    author = db.Column(db.String(64), nullable=False, index=True)
    is_read = db.Column(db.Boolean, default=False)

    def __init__(self, title, author, is_read):
        self.title = title
        self.author = author
        self.is_read = is_read

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.title)


@app.route('/', methods=['GET'])
def show_books():
    flash_mes = request.args['flash_mes'] if 'flash_mes' in request.args.to_dict().keys() else ''
    books = Book.query.all()
    return render_template('show_books.html', books=books, flash_mes=flash_mes)


@app.route('/add', methods=['POST', 'GET'])
def add_book():
    title = request.form['title'] if 'title' in request.form.to_dict().keys() else ''
    author = request.form['author'] if 'author' in request.form.to_dict().keys() else ''
    is_read = 1 if 'is_read' in request.form.to_dict().keys() else 0
    flash_mes = ""
    if title and author:
        new_books = Book(title, author, is_read)
        db.session.add(new_books)
        db.session.commit()
        flash_mes = "新书添加成功"
    else:
        flash_mes = "请填写书名与作者"
    return redirect(url_for('show_books', flash_mes=flash_mes))


@app.route('/delete/<int:bookid>')
def delete_book(bookid):
    delete_books = Book.query.filter(Book.id == bookid).first()
    db.session.delete(delete_books)
    db.session.commit()
    return redirect(url_for('show_books', flash_mes="删除成功"))


@app.route('/update/<int:bookid>', methods=['POST'])
def update_book(bookid):
    flash_mes = ""
    update_books = Book.query.filter(Book.id == bookid).first()
    title = request.form['title'] if 'title' in request.form.to_dict().keys() else ''
    author = request.form['author'] if 'author' in request.form.to_dict().keys() else ''
    is_read = 1 if 'is_read' in request.form.to_dict().keys() else 0
    db.session.commit()
    if title and author:
        update_books.title = title
        update_books.author = author
        update_books.is_read = is_read
        db.session.commit()
        flash_mes = "修改成功"
    else:
        flash_mes = "请填写书名与作者"
    return redirect(url_for('show_books', flash_mes=flash_mes))


if __name__ == '__main__':
    app.run()
