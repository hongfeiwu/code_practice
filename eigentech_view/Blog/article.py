# coding=utf-8
from flask import Blueprint

bp = Blueprint('article', __name__, url_prefix='/article')


@bp.route('/')
def index():
    return 'article"s Index page'
