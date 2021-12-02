import unittest
from unittest import mock
from flask_opsgenie.opsgenie import make_opsgenie_api_request

class TestOpsgenie(unittest.TestCase):

    @mock.patch('flask_opsgenie.opsgenie.requests.post')
    @mock.patch('flask_opsgenie.opsgenie.requests.get')
    def test_make_opsgenie_api_request(self, mock_get, mock_post):

        _ = make_opsgenie_api_request(http_verb="get", url=mock.ANY, payload=mock.ANY, opsgenie_token=mock.ANY)
        self.assertEqual(mock_get.call_count, 1)
        _ = make_opsgenie_api_request(http_verb="post", url=mock.ANY, payload=mock.ANY, opsgenie_token=mock.ANY)
        self.assertEqual(mock_post.call_count, 1)
