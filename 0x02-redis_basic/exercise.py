#!/usr/bin/env python3
''' redis module '''

import redis
import uuid
from typing import Union


class Cache():
    ''' a cache class '''
    def __init__(self):
        ''' initialize redis instance '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' generates a random key '''
        gen_key = str(uuid.uuid4())
        self._redis.set(gen_key, data)
        return gen_key
