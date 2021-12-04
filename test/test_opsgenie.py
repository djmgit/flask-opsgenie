import unittest
from flask import Flask
from unittest import mock
from flask_opsgenie.entities import OpsgenieAlertParams
from flask_opsgenie.opsgenie import make_opsgenie_api_request
from flask_opsgenie.opsgenie import raise_opsgenie_status_alert

class TestOpsgenie(unittest.TestCase):

    def setUp(self):
        self.opsgenie_alert_params = OpsgenieAlertParams(
            opsgenie_token=mock.ANY,
            alert_tags=mock.ANY,
            alert_details={"service_id":"fake_service", "host": "test-host"},
            alert_alias=None,
            alert_status_alias=None,
            alert_latency_alias=None,
            alert_exception_alias=None,
            alert_priority="P4",
            alert_responder=mock.ANY,
            opsgenie_api_base="https://dummy-opsgenie.com"
        )

    @mock.patch('flask_opsgenie.opsgenie.requests.post')
    @mock.patch('flask_opsgenie.opsgenie.requests.get')
    def test_make_opsgenie_api_request(self, mock_get, mock_post):

        _ = make_opsgenie_api_request(http_verb="get", url=mock.ANY, payload=mock.ANY, opsgenie_token=mock.ANY)
        self.assertEqual(mock_get.call_count, 1)
        _ = make_opsgenie_api_request(http_verb="post", url=mock.ANY, payload=mock.ANY, opsgenie_token=mock.ANY)
        self.assertEqual(mock_post.call_count, 1)

    @mock.patch('flask_opsgenie.opsgenie.make_opsgenie_api_request')
    def test_raise_opsgenie_status_alert(self, mock_opsgenie_api_request):

        app = Flask(__name__)
        with app.test_client() as client:
            rv = client.get('/test/og_params')
            _ = raise_opsgenie_status_alert(alert_status_code=500, alert_status_class=None, opsgenie_alert_params=self.opsgenie_alert_params)
            self.assertEqual(self.opsgenie_alert_params.alert_details['endpoint'], '/test/og_params')
            self.assertEqual(self.opsgenie_alert_params.alert_details['method'], "GET")
            self.assertEqual(self.opsgenie_alert_params.alert_details['url'], 'http://localhost/test/og_params')
            self.assertEqual(self.opsgenie_alert_params.alert_details['status_code'], 500)
            self.assertEqual(self.opsgenie_alert_params.alert_details.get('status_class'), None)
            self.assertEqual(self.opsgenie_alert_params.alert_status_alias, 'fake_service-response-status-alert')
            self.assertEqual(mock_opsgenie_api_request.call_count, 1)
