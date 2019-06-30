# -*- coding: utf-8 -*-
import importlib
from threading import Thread
from flask import request
from flask_migrate import MigrateCommand
import app
import api
import model
import setting
from Blog import app, db, manager, migrate, login_manager, sess


def create_app():
    app.config.from_object("settings.common")
    app.config.from_object("settings.%s" % flask_env)

    if app.config.get("STATIC_FOLDER"):
        app.static_folder = app.config.get("STATIC_FOLDER")
    if app.config.get("TEMPLATE_FOLDER"):
        app.template_folder = app.config.get("TEMPLATE_FOLDER")

    sess.init_app(app)
    migrate.init_app(app, db)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


# 所有请求都会经过，然后用来处理api调用
@app.before_request
def visit_api():
    if request.blueprint == 'api':
        print("api")
