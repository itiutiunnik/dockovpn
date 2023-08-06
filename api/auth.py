import os
from flask import request
from .variables import APIKEY_HEADER
import functools

def is_valid(key):
    try:
        return key == os.environ["APIKEY"]
    except:
        return False
    
def apikey_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        key = request.headers.get(APIKEY_HEADER)
        if is_valid(key):
            return func(*args, **kwargs)
        else:
            return {'message':'Access denied'}, 403
    return decorator