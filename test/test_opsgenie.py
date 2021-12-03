import unittest
from unittest import mock
from flask_opsgenie.entities import OpsgenieAlertParams
from flask_opsgenie.opsgenie import make_opsgenie_api_request
from flask_opsgenie.opsgenie import raise_opsgenie_status_alert

class TestOpsgenie(unittest.TestCase):

    @mock.patch('flask_opsgenie.opsgenie.requests.post')
    @mock.patch('flask_opsgenie.opsgenie.requests.get')
    def test_make_opsgenie_api_request(self, mock_get, mock_post):

        _ = make_opsgenie_api_request(http_verb="get", url=mock.ANY, payload=mock.ANY, opsgenie_token=mock.ANY)
        self.assertEqual(mock_get.call_count, 1)
        _ = make_opsgenie_api_request(http_verb="post", url=mock.ANY, payload=mock.ANY, opsgenie_token=mock.ANY)
        self.assertEqual(mock_post.call_count, 1)

    @mock.patch('flask_opsgenie.opsgenie.make_opsgenie_api_request')
    @mock.patch('flask_opsgenie.opsgenie.request')
    def test_raise_opsgenie_status_alert(self, mock_flask_request, mock_opsgenie_api_request):

        mock_flask_request.path = mock.ANY
        mock_flask_request.method = mock.ANY
        mock_flask_request.url = mock.ANY

        opsgenie_alert_params = OpsgenieAlertParams(
            opsgenie_token=mock.ANY,
            alert_tags=mock.ANY,
            alert_details={"service_id":"fake_service"},
            alert_alias=None,
            alert_status_alias=None,
            alert_latency_alias=None,
            alert_exception_alias=None,
            alert_priority="P4",
            alert_responder=mock.ANY,
            opsgenie_api_base="https://dummy-opsgenie.com"
        )

        _ = raise_opsgenie_status_alert(alert_status_code=500, alert_status_class=None, opsgenie_alert_params=opsgenie_alert_params)

        self.assertEqual(opsgenie_alert_params.alert_details["endpoint"], mock_flask_request.path)
