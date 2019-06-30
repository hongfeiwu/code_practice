# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.migrate import Migrate
from flask_script import Manager
from flask.ext.login import LoginManager
from werkzeug.contrib.cache import SimpleCache
from flask.ext.session import Session

app = Flask(__name__)
manager = Manager(app)
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
cache = SimpleCache()
sess = Session()

import create_app
