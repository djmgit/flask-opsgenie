from logging import exception
import unittest
from flask import Flask
from unittest import mock
from flask_opsgenie import opsgenie
from flask_opsgenie.entities import OpsgenieAlertParams, AlertType
from flask_opsgenie.opsgenie import make_opsgenie_api_request
from flask_opsgenie.opsgenie import (raise_opsgenie_status_alert, raise_opsgenie_latency_alert,
                                     raise_opsgenie_exception_alert, raise_opsgenie_alert)

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
            mock_opsgenie_api_request.assert_called_with(
                http_verb="post",
                url=f'{self.opsgenie_alert_params.opsgenie_api_base}/v2/alerts',
                payload=mock.ANY,
                opsgenie_token=self.opsgenie_alert_params.opsgenie_token
            )


    @mock.patch('flask_opsgenie.opsgenie.make_opsgenie_api_request')
    def test_raise_opsgenie_exception_alert(self, mock_opsgenie_api_request):

        app = Flask(__name__)
        with app.test_client() as client:
            rv = client.get('/test/og_params')
            _ = raise_opsgenie_latency_alert(elapsed_time=2000, alert_status_code=500, opsgenie_alert_params=self.opsgenie_alert_params)
            self.assertEqual(self.opsgenie_alert_params.alert_details['endpoint'], '/test/og_params')
            self.assertEqual(self.opsgenie_alert_params.alert_details['method'], "GET")
            self.assertEqual(self.opsgenie_alert_params.alert_details['url'], 'http://localhost/test/og_params')
            self.assertEqual(self.opsgenie_alert_params.alert_details['status_code'], 500)
            self.assertEqual(self.opsgenie_alert_params.alert_details.get('status_class'), None)
            self.assertEqual(self.opsgenie_alert_params.alert_latency_alias, 'fake_service-response-latency-alert')
            self.assertEqual(mock_opsgenie_api_request.call_count, 1)
            mock_opsgenie_api_request.assert_called_with(
                http_verb="post",
                url=f'{self.opsgenie_alert_params.opsgenie_api_base}/v2/alerts',
                payload=mock.ANY,
                opsgenie_token=self.opsgenie_alert_params.opsgenie_token
            )

    @mock.patch('flask_opsgenie.opsgenie.make_opsgenie_api_request')
    def test_raise_opsgenie_latency_alert(self, mock_opsgenie_api_request):

        test_exception = mock.ANY
        app = Flask(__name__)
        with app.test_client() as client:
            rv = client.get('/test/og_params')
            _ = raise_opsgenie_exception_alert(exception=test_exception, opsgenie_alert_params=self.opsgenie_alert_params)
            self.assertEqual(self.opsgenie_alert_params.alert_details['endpoint'], '/test/og_params')
            self.assertEqual(self.opsgenie_alert_params.alert_details['method'], "GET")
            self.assertEqual(self.opsgenie_alert_params.alert_details['url'], 'http://localhost/test/og_params')
            self.assertEqual(self.opsgenie_alert_params.alert_details['exception'], test_exception)
            self.assertEqual(self.opsgenie_alert_params.alert_exception_alias, 'fake_service-exception-alert')
            self.assertEqual(mock_opsgenie_api_request.call_count, 1)
            mock_opsgenie_api_request.assert_called_with(
                http_verb="post",
                url=f'{self.opsgenie_alert_params.opsgenie_api_base}/v2/alerts',
                payload=mock.ANY,
                opsgenie_token=self.opsgenie_alert_params.opsgenie_token
            )

    @mock.patch('flask_opsgenie.opsgenie.raise_opsgenie_status_alert')
    @mock.patch('flask_opsgenie.opsgenie.raise_opsgenie_latency_alert')
    @mock.patch('flask_opsgenie.opsgenie.raise_opsgenie_exception_alert')
    def test_raise_opsgenie_alert(self, mock_opsgenie_exception_alert, mock_opsgenie_latency_alert, mock_opsgenie_status_alert):

        test_exception = mock.ANY
        test_status_code = 500
        test_status_calss = "5XX"
        test_elapsed_time = 2000

        _ = raise_opsgenie_alert(alert_type=AlertType.STATUS_ALERT, alert_status_code=test_status_code,
                                 elapsed_time = None, opsgenie_alert_params=self.opsgenie_alert_params)
        self.assertEqual(mock_opsgenie_status_alert.call_count, 1)
        mock_opsgenie_status_alert.assert_called_with(
            alert_status_code=test_status_code,
            opsgenie_alert_params=self.opsgenie_alert_params
        )
        _ = raise_opsgenie_alert(alert_type=AlertType.STATUS_ALERT, alert_status_class=test_status_calss,
                                 elapsed_time = None, opsgenie_alert_params=self.opsgenie_alert_params)
        self.assertEqual(mock_opsgenie_status_alert.call_count, 2)
        mock_opsgenie_status_alert.assert_called_with(
            alert_status_class=test_status_calss,
            opsgenie_alert_params=self.opsgenie_alert_params
        )
        _ = raise_opsgenie_alert(alert_type=AlertType.LATENCY_ALERT, alert_status_code=test_status_code,
                                 elapsed_time=test_elapsed_time, opsgenie_alert_params=self.opsgenie_alert_params)
        self.assertEqual(mock_opsgenie_latency_alert.call_count, 1)
        mock_opsgenie_latency_alert.assert_called_with(
            elapsed_time=test_elapsed_time,
            alert_status_code=test_status_code,
            opsgenie_alert_params=self.opsgenie_alert_params
        )
        _ = raise_opsgenie_alert(alert_type=AlertType.EXCEPTION, exception=test_exception, opsgenie_alert_params=self.opsgenie_alert_params)
        self.assertEqual(mock_opsgenie_exception_alert.call_count, 1)
        mock_opsgenie_exception_alert.assert_called_with(
            exception=test_exception,
            opsgenie_alert_params=self.opsgenie_alert_params
        )
