import os
import unittest
from elex.api import utils
from . import API_MESSAGE

AP_API_LIMIT = 11
QUOTA_MESSAGE = 'You must set AP_RUN_QUOTA_TEST=1 in your environment to \
run the quota test.'


class APQuotaTestCase(unittest.TestCase):

    def setUp(self):
        self.responses = []
        for i in range(AP_API_LIMIT):
            self.responses.append(utils.api_request('/'))

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    @unittest.skipUnless(
        os.environ.get('AP_RUN_QUOTA_TEST', None),
        QUOTA_MESSAGE
    )
    def test_quota_status_code(self):
        self.assertEqual(self.responses[-1].status_code, 403)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    @unittest.skipUnless(
        os.environ.get('AP_RUN_QUOTA_TEST', None),
        QUOTA_MESSAGE
    )
    def test_only_one_quota_failures(self):
        num_quota_failures = 0
        for response in self.responses:
            if response.status_code == 403:
                num_quota_failures += 1

        self.assertEqual(num_quota_failures, 1)
