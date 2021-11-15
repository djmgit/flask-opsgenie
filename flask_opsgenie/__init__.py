import os
from typing import Optional

from flask import Flask, request, Response, g, _app_ctx_stack as stack

class FlaskOpsgenie(object):

    def __init__(self, app: Optional[Flask]):

        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):

        self.alert_statuse_codes = None
        self.alert_status_classes = None
        self.monitord_endpoints = None
        self.ignored_endpoints = None
        self.threshold_response_time = None
        self.response_time_monitored_endpoints = None

        app.before_request(self._before_request)
        app.after_request(self._after_request)
        app.teardown_request(self._teardown_request)

    def _before_request(self):
        print ("before reuqest from extension")

    def _after_request(self, response: Response):
        print ("after request from extension")
        return response
