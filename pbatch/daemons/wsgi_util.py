import json

import webob
from webob.dec import wsgify
import routes

class Dispatcher(object):
    def __init__(self):
        self.map = routes.Mapper()        

    @wsgify
    def __call__(self, req):
        results = self.map.routematch(environ=req.environ)
        #print "RES:", repr(results), dir(results)
        if not results:
            return webob.exc.HTTPNotFound()
        match, route = results
        req.urlvars = ((), match)
        kwargs = match.copy()
        view = kwargs.pop('controller')
        #print "V:", repr(view), dir(view)
        method_name = kwargs.pop('method')
        method = getattr(view(), method_name)

        method_return = method(req, **kwargs)
        
        if isinstance(method_return, webob.Response):
            return method_return
        else:
            return webob.Response(method_return)

def json_post(method):
    """ The data in the post will be passed as a post_data argument to 
    the decorated method."""
    def wrap(*args, **kwargs):
        # idx is the position of the data
        idx = 0
        if not isinstance(args[0], webob.Request):
            idx = 1

        json_data = json.loads(args[idx].body)
        kwargs['post_data'] = json_data

        #print "JP:", repr(args), repr(kwargs)

        return method(*args, **kwargs)
    
    return json_return(wrap)

def json_return(method):
    def wrap(*args, **kwargs):
        resp = webob.Response()
        resp.body = json.dumps(method(*args, **kwargs))
        resp.content_type = "application/json"
        return resp
    return wrap

