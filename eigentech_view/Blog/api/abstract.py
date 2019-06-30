# -*- coding: utf-8 -*-
import json
from bson import json_util
from flask_restful import Resource
from backend.core.exceptions import ApiUserError, UserError
from backend.views.abstract import ViewMixin


class ActionApi(Resource, ViewMixin):
    def __init__(self):
        pass

    def raise_error(self, *args, **kwargs):
        raise ApiUserError(*args, **kwargs)

    def raise404(self, msg=u"该接口不存在"):
        self.raise_error(msg)

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def dispatch_action(self, action, *args, **kwargs):
        try:
            if not hasattr(self, action):
                self.raise404()
            return getattr(self, action)(*args, **kwargs)

        except UserError as err:
            return self.fail(err.message, err.status_code)
        except NotImplementedError:
            return self.fail(u"接口未实现")

    def get(self, action=None, **kwargs):
        return self.dispatch_action(action, **kwargs)

    def post(self, action=None, **kwargs):
        return self.dispatch_action(action, **kwargs)

    def done(self, data=None):
        if isinstance(data, Resource):
            return data
        return json.loads(json.dumps({'success': True, "data": data}, default=json_util.default))

    def fail(self, message=None, code=400):
        if isinstance(message, Resource):
            return message
        return json.loads(json.dumps({'success': False, "message": message, "code": code}, default=json_util.default))
