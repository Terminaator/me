import json
from functools import wraps

def RequestJson(view_func):

    @wraps(view_func)
    def wrapper_view_func(request, *args, **kwargs):
        if request.content_type == 'application/json':
            if request.body:
                request.json = json.loads(request.body.decode('utf-8'))
            else:
                request.json = None
        return view_func(request, *args, **kwargs)
    return wrapper_view_func