#!/usr/bin/env python3
"""implementing an expiring web cache and tracker"""

from typing import Callable
from functools import wraps
import redis
import requests


def requests_counter(method: Callable) -> Callable:
    """ Count requests number """
    r = redis.Redis()

    @wraps(method)
    def wrapper(url):
        """wrapper function that counts actual number of requests made"""
        r.incr(f"count:{url}")
        cached_ = r.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')

        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@requests_counter
def get_page(url: str) -> str:
    """ return html content for a given url"""
    resp = requests.get(url)
    return resp.text
