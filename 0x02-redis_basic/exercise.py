#!/usr/bin/env python3
''' redis module '''

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    ''' decorator function that returns callable '''
    @wraps(method)
    def wrapper(self, *args, **kwds):
        ''' wrapper function '''
        my_key = method.__qualname__
        self._redis.incr(my_key)
        return method(self, *args, **kwds)
    return wrapper
    
class Cache():
    ''' a cache class '''
    def __init__(self):
        ''' initialize redis instance '''
        self._redis = redis.Redis()
        self._redis.flushdb()
        
    @count_calls    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' generates a random key '''
        gen_key = str(uuid.uuid4())
        self._redis.set(gen_key, data)
        return gen_key

    def get(self, key:str, fn:Optional[Callable]=None) -> Union[str, bytes, int, float]:
        ''' get method key value '''
        val = self._redis.get(key)
        return val if not fn else fn(val)

    def get_str(self, key) -> str:
        ''' returns value string '''
        str_val = self._redis.get(key)
        return str_val.decode('utf-8')

    def get_int(self, key) -> int:
        ''' returns int '''
        return self.get(key, int)
    
