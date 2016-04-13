"""
Elex exceptions
"""
from __future__ import unicode_literals


class APAPIKeyException(Exception):
    """
    Raise this exception when an AP API key is not set.
    """
    message = 'AP API key is not set.'

    def __str__(self):
        return self.message
