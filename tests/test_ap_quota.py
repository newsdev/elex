import os
import unittest

from elex.api import utils
from . import API_MESSAGE

AP_API_LIMIT = 20
QUOTA_MESSAGE = 'You must set AP_RUN_QUOTA_TEST=1 in your environment to run the quota test.'


class APQuotaTestCase(unittest.TestCase):

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    @unittest.skipUnless(os.environ.get('AP_RUN_QUOTA_TEST', None), QUOTA_MESSAGE)
    def test_quota_status_code(self):
        for i in range(AP_API_LIMIT):
            response = utils.api_request('/')
        self.assertEqual(response.status_code, 403)
