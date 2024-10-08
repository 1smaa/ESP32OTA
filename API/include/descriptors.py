import functools
from flask import jsonify
from typing import Callable, Any
import sys
import traceback

from include.const import *
from include.exceptions import *

#
# INCLUDES ALL FUNCTION DESCRIPTORS USED 
#

def endpoint_wrap(f: Callable) -> Callable:
    '''
    Wraps endpoints of the RESTful API to make easier handling different return codes by signaling them as exceptions
    '''
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        try:
            return f(*args,**kwargs),SUCCESSFUL
        except Unauthorized as e:
            return jsonify({
                "response":"Unauthorized Request"
            }), UNAUTHORIZED
        except BadRequest as e:
            return jsonify({
                "response":"Bad Request"
            }), BAD_REQUEST
        except Exception as e:
            return jsonify({
                "response":"Internal Server Error",
                "exception":traceback.format_exc()
            }), INTERNAL_ERROR
    return wrapper

def no_except(f: Callable) -> Callable:
    '''
    Wraps function for which we want a no-throw guarantee
    '''
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except:
            return None
    return wrapper

def bool_except(f: Callable) -> Callable:
    '''
    Returns true if the function completes without exceptions,false otherwise. Used only for "void" functions
    '''
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        try:
            f(*args,**kwargs)
        except Exception as e:
            raise Exception(sys.exc_info())
            return False
        else:
            return True
    return wrapper