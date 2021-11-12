import os
from typing import Optional

from flask import Flask, request, Response, g, _app_ctx_stack as stack

class FlaskOpsgenie(object):

    def __init__(self, app: Optional[Flask]):

        self.app = app

        if app is None:
            self.init_app(app)

    def init_app(self, app: Flask):

        app.before_request(self._before_request)
        app.after_request(self._after_request)

    def _before_request(self):
        pass

    def _after_request(self):
        pass
