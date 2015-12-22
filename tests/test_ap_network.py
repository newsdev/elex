import json
import os
import unittest

from elex.api import utils
from tests import ElectionNetworkTestCase

class APNetworkTestCase(ElectionNetworkTestCase):

    message = "We require that you export AP_API_KEY in your environment in order to test AP connectivity."

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), message)
    def test_bad_date_error_code(self):
        self.assertEqual(self.bad_date_response.status_code, 400)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), message)
    def test_bad_date_error_message(self):
        self.assertEqual(self.bad_date_response.reason, 400)

        #r = response.json()
        #self.assertTrue('errorCode' in r)
        #self.assertTrue('errorMessage' in r)
        #self.assertEqual(r['errorCode'], 400)
        #self.assertEqual(r['errorMessage'], 'String was not recognized as a valid DateTime.')
        #self.assertFalse('races' in r)

    #@unittest.skipUnless(os.environ.get('AP_API_KEY', None), message)
    #def test_nonexistent_date(self):
        #response = utils.api_request('/1965-01-01')
        #r = response.json()
        #self.assertTrue('races' in r)
        #self.assertEqual(len(r['races']), 0)

    #@unittest.skipUnless(os.environ.get('AP_API_KEY', None), message)
    #def test_nonexistent_param(self):
        #response = utils.api_request('/', foo='bar')
        #r = response.json()
        #self.assertTrue('errorCode' in r)
        #self.assertTrue('errorMessage' in r)
        #self.assertEqual(r['errorCode'], 400)
        #self.assertEqual(r['errorMessage'], 'Specified parameter(s) \'foo\' is invalid')
        #self.assertFalse('races' in r)
