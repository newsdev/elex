from cachecontrol.heuristics import BaseHeuristic


class EtagOnlyCache(BaseHeuristic):
    """
    Strip max-age cache-control header if it exists alongside etag.
    """
    def update_headers(self, response):
        headers = {}
        max_age = 'max-age' in response.headers.get('cache-control', '')
        etag = response.headers.get('etag', None)
        if max_age and etag:
            headers['cache-control'] = 'public'
        return headers
