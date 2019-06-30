# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api

from .users import *

bp_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api1 = Api(bp_v1)

# 用户
api1.add_resource(UserApi,
                  "/user",
                  "/user/<string:action>")
