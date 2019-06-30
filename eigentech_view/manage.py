#!/usr/bin/env python
# coding: utf8

import os
import sys
from flask.ext.script import Server

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

from Blog import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'development')

if __name__ == "__main__":
    from Blog import manager

    manager.add_command('runserver', Server(host='0.0.0.0'))
    manager.run()
