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


def call_history(method: Callable) -> Callable:
    ''' another decorator function that returns a callble '''
    @wraps(method)
    def wrapper(self, *args, **kwds):
        ''' wrapper function '''
        my_key = method.__qualname__
        input_key = my_key + ":inputs"
        output_key = my_key + ":outputs"
        data = str(args)
        self._redis.rpush(input_key, data)
        output_list = method(self, *args, **kwds)
        self._redis.rpush(output_key, str(output_list))
        return output_list
    return wrapper


def replay(func: Callable):
    ''' displays history of call of a particular function '''
    r = redis.Redis()
    my_key = func.__qualname__
    inp_key = r.lrange("{}:inputs".format(my_key), 0, -1)
    outp_key = r.lrange("{}:outputs".format(my_key), 0, -1)
    num_calls = len(inp_key)
    num_times = 'times'
    if num_calls < 2:
        num_times = 'time'
    my_output = '{} was called {} {}:'.format(my_key, num_calls, num_times)
    print(my_output)
    for ky, val in zip(inp_key, outp_key):
        my_output = '{}(*{}) -> {}'.format(
            my_key,
            ky.decode('utf-8'),
            val.decode('utf-8')
        )
        print(my_output)


class Cache():
    ''' a cache class '''
    def __init__(self):
        ''' initialize redis instance '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' generates a random key '''
        gen_key = str(uuid.uuid4())
        self._redis.set(gen_key, data)
        return gen_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
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
