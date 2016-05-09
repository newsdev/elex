from cachecontrol.heuristics import BaseHeuristic


class EtagOnlyCache(BaseHeuristic):
    """
    Strip max-age cache-control header if it exists alongside etag.
    """
    def update_headers(self, response):
        headers = {}
        if 'max-age' in response.headers.get('cache-control') and response.headers.get('etag'):
            headers['cache-control'] = 'public'
        return headers
