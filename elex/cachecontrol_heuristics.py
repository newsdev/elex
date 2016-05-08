from cachecontrol.heuristics import BaseHeuristic


class EtagOnlyCache(BaseHeuristic):
    """
    Cache the response by providing an expires 1 day in the
    future.
    """
    def update_headers(self, response):
        return {
            'cache-control': 'public',
            'etag': response.headers.get('etag'),
        }
