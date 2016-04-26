import os
import unittest

from requests.exceptions import HTTPError
from time import sleep
from . import NetworkTestCase, API_MESSAGE


class APNetworkTestCase(NetworkTestCase):

    def tearDown(self, **kwargs):
        sleep(5)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_bad_date_error_code(self):
        with self.assertRaises(HTTPError) as error:
            self.api_request('/elections/9999-99-99')
        response = error.exception.response
        if response.status_code == 403:
            self.skipTest('over quota limit')
        self.assertEqual(response.status_code, 404)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_nonexistent_date(self):
        nonexistent_date_response = self.api_request('/elections/1965-01-01')
        data = nonexistent_date_response.json()
        self.assertEqual(len(data['races']), 0)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_nonexistent_param(self):
        with self.assertRaises(HTTPError) as error:
            self.api_request('/elections/', foo='bar')
        response = error.exception.response
        if response.status_code == 403:
            self.skipTest('over quota limit')
        self.assertEqual(response.status_code, 400)
