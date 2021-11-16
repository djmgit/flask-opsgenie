import os
import socket
import time
from typing import Optional

from flask import Flask, request, Response, g, _app_ctx_stack as stack

CONFIG_ALERT_STATUS_CODES = "ALERT_STATUS_CODES"
CONFIG_ALERT_STATUS_CLASSES = "ALERT_STATUS_CLASSES"
CONFIG_MONITORED_ENDPOINTS = "MONITORED_ENDPOINTS"
CONFIG_IGNORED_ENDPOINTS = "IGNORED_ENDPOINTS"
CONFIG_THRESHOLD_RESPONSE_TIME = "THRESHOLD_RESPONSE_TIME"
CONFIG_RESPONSE_TIME_MONITORED_ENDPOINTS = "RESPONSE_TIME_MONITORED_ENDPOINTS"
CONFIG_OPSGENIE_TOKEN = "OPSGENIE_TOKEN"

class FlaskOpsgenie(object):

    def __init__(self, app: Optional[Flask]):

        self.app = app
        self._host = None
        self._alert_statuse_codes = None
        self._alert_status_classes = None
        self._monitored_endpoints = None
        self._ignored_endpoints = None
        self._threshold_response_time = None
        self._response_time_monitored_endpoints = None
        self._opsgenie_token = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):

        self._alert_status_codes = app.config.get(CONFIG_ALERT_STATUS_CODES)
        self._alert_status_classes = app.config.get(CONFIG_ALERT_STATUS_CLASSES)
        self._monitored_endpoints = app.config.get(CONFIG_MONITORED_ENDPOINTS)
        self._ignored_endpoints = app.config.get(CONFIG_IGNORED_ENDPOINTS)
        self._threshold_response_time = app.config.get(CONFIG_THRESHOLD_RESPONSE_TIME)
        self._response_time_monitored_endpoints = app.config.get(CONFIG_RESPONSE_TIME_MONITORED_ENDPOINTS)
        self._opsgenie_token = app.config.get(CONFIG_OPSGENIE_TOKEN)
        self._opsgenie_token = app.config.get("")
        self._host = socket.gethostbyname()

        app.before_request(self._before_request)
        app.after_request(self._after_request)
        app.teardown_request(self._teardown_request)

    def _get_status_class(status_code: int) -> str:
        return ""

    def _before_request(self):
        ctx = stack.top
        ctx._flask_request_begin_at = time.time()

    def _after_request(self, response: Response):
        ctx = stack.top
        elapsed_time = (time.time() - ctx._flask_request_begin_at) * 1000

        status_code = response.status_code
        status_class = self._get_status_class(status_code)
        request_endpoint = request.endpoint
