import os
import socket
import time
from typing import Optional

from flask import Flask, request, Response, g, _app_ctx_stack as stack
from flask_opsgenie.opsgenie import raise_opsgenie_alert
from flask_opsgenie.entities import AlertType

CONFIG_ALERT_STATUS_CODES = "ALERT_STATUS_CODES"
CONFIG_ALERT_STATUS_CLASSES = "ALERT_STATUS_CLASSES"
CONFIG_MONITORED_ENDPOINTS = "MONITORED_ENDPOINTS"
CONFIG_IGNORED_ENDPOINTS = "IGNORED_ENDPOINTS"
CONFIG_THRESHOLD_RESPONSE_TIME = "THRESHOLD_RESPONSE_TIME"
CONFIG_RESPONSE_TIME_MONITORED_ENDPOINTS = "RESPONSE_TIME_MONITORED_ENDPOINTS"
CONFIG_OPSGENIE_TOKEN = "OPSGENIE_TOKEN"
CONFIG_ALERT_TAGS = "ALERT_TAGS"
CONFIG_ALERT_PRIORITY = "ALERT_PRIORITY"
CONFIG_ALERT_ALIAS = "ALERT_ALIAS"
CONFIG_RESPONDER = "RESPONDER"
CONFIG_OPSGENIE_API_BASE = "OPSGENIE_API_BASE"
CONFIG_SERVICE_ID = "SERVICE_ID"
OPSGENIE_API_BASE_US = "https://api.opsgenie.com"


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
        self._alert_tags = None
        self._alert_priority = None
        self._alert_alias = None
        self._responder = None
        self._opsgenie_api_base = None
        self._service_id = None

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
        self._alert_tags = app.config.get(CONFIG_ALERT_TAGS, {})
        self._alert_alias = app.config.get(CONFIG_ALERT_ALIAS)
        self._alert_priority = app.config.get(CONFIG_ALERT_PRIORITY, "P4")
        self._responder = app.config.get(CONFIG_RESPONDER)
        self._opsgenie_api_base = app.config.get(CONFIG_OPSGENIE_API_BASE, OPSGENIE_API_BASE_US)
        self._service_id = app.config.get(CONFIG_SERVICE_ID)
        self._host = socket.gethostname()

        # add host to alert tags as well
        self._alert_tags["host"] = self._host

        app.before_request(self._before_request)
        app.after_request(self._after_request)
        app.teardown_request(self._teardown_request)

    def _get_status_class(status_code: int) -> str:
        return str(status_code)[0] + "XX"

    def _before_request(self):
        ctx = stack.top
        ctx._flask_request_begin_at = time.time()

    def _after_request(self, response: Response):
        ctx = stack.top
        elapsed_time = (time.time() - ctx._flask_request_begin_at) * 1000

        status_code = response.status_code
        status_class = self._get_status_class(status_code)
        endpoint = request.path

        if (self._alert_status_codes and status_code in self._alert_status_codes) or \
                (self._alert_status_classes and status_class in self._alert_status_classes):
            if (self._monitored_endpoints and endpoint in self._monitored_endpoints) or \
                    (not self._monitored_endpoints and endpoint not in self._ignored_endpoints):
                if self._alert_status_codes:
                    raise_opsgenie_alert(AlertType.STATUS_ALERT, alert_status_code=status_code, tags=self._alert_tags)
                elif self._alert_status_classes:
                    raise_opsgenie_alert(AlertType.STATUS_ALERT, alert_status_class=status_class, tags=self._alert_tags)

        if self._threshold_response_time and endpoint in self._response_time_monitored_endpoints:
            raise_opsgenie_alert(AlertType.LATENCY_ALERT, elapsed_time=elapsed_time, tags=self._alert_tags)
