import os
import unittest

from . import NetworkTestCase, API_MESSAGE


class APNetworkTestCase(NetworkTestCase):

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_bad_date_error_code(self):
        self.assertEqual(self.api_request('/9999-99-99').status_code, 400)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_bad_date_error_message(self):
        bad_date_response = self.api_request('/9999-99-99')
        data = bad_date_response.json()
        self.assertEqual(
            data['errorMessage'],
            'String was not recognized as a valid DateTime.'
        )

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_bad_date_fields(self):
        bad_date_response = self.api_request('/9999-99-99')
        data = bad_date_response.json()
        keys = data.keys()
        self.assertTrue('errorMessage' in keys and 'errorCode' in keys)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_nonexistent_date(self):
        nonexistent_date_response = self.api_request('/1965-01-01')
        data = nonexistent_date_response.json()
        self.assertEqual(len(data['races']), 0)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_nonexistent_param(self):
        nonexistent_param_response = self.api_request('/', foo='bar')
        self.assertEqual(nonexistent_param_response.status_code, 400)
