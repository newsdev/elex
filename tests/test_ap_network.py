import json
import unittest

from elex.parser import utils

class APNetworkTestCase(unittest.TestCase):

    def test_bad_date(self):
        r = utils.api_request('/9999-99-99')
        self.assertTrue('errorCode' in r)
        self.assertTrue('errorMessage' in r)
        self.assertEqual(r['errorCode'], 400)
        self.assertEqual(r['errorMessage'], 'String was not recognized as a valid DateTime.')
        self.assertFalse('races' in r)

    def test_nonexistent_date(self):
        r = utils.api_request('/1965-01-01')
        self.assertTrue('races' in r)
        self.assertEqual(len(r['races']), 0)

    def test_nonexistent_param(self):
        r = utils.api_request('/', foo='bar')
        self.assertTrue('errorCode' in r)
        self.assertTrue('errorMessage' in r)
        self.assertEqual(r['errorCode'], 400)
        self.assertEqual(r['errorMessage'], 'Specified parameter(s) \'foo\' is invalid')
        self.assertFalse('races' in r)