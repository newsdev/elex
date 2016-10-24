import os
import unittest

from elex.cli.app import ElexApp
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


class ElexNetworkCacheTestCase(NetworkTestCase):
    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_elex_cache_miss(self):
        from elex import cache
        response = self.api_request('/elections/2016-02-01')
        http_adapter = cache.get_adapter('http://')
        try:
            http_adapter.cache.delete(response.url)
        except OSError:
            pass
        uncached_response = self.api_request('/elections/2016-02-01')
        self.assertEqual(uncached_response.from_cache, False)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_elex_cache_hit(self):
        self.api_request('/elections/2016-02-01')
        cached_response = self.api_request('/elections/2016-02-01')
        self.assertEqual(cached_response.from_cache, True)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_elex_cache_hit_exit_code(self):
        uncached_app = ElexApp(argv=['results', '2016-02-01', '--quiet'])
        uncached_app.setup()
        uncached_app.run()
        cached_app = ElexApp(argv=['results', '2016-02-01', '--quiet'])
        cached_app.setup()
        cached_app.run()
        self.assertEqual(cached_app.exit_code, 64)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_elex_cache_clear_command_after_caching(self):
        self.api_request('/elections/2016-02-01')
        app = ElexApp(argv=['clear-cache', '--quiet'])
        app.setup()
        app.run()
        self.assertEqual(app.exit_code, 0)

    @unittest.skipUnless(os.environ.get('AP_API_KEY', None), API_MESSAGE)
    def test_elex_cache_clear_command_no_cache(self):
        app = ElexApp(argv=['clear-cache', '--quiet'])
        app.setup()
        app.run()
        self.assertEqual(app.exit_code, 65)
