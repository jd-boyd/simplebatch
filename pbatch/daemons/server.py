import argparse
import json
import os

import webob
from webob.dec import wsgify
import routes

import pbatch.model

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

dispatcher = Dispatcher()

def json_post(method):
    def wrap(*args, **kwargs):
        # idx is the position of the data
        idx = 0
        if not isinstance(args[0], webob.Request):
            idx = 1

        json_data = json.loads(args[idx].body)
        args = args + (json_data,)
        return method(*args)
    
    return json_return(wrap)

def json_return(method):
    def wrap(*args, **kwargs):
        resp = webob.Response()
        resp.body = json.dumps(method(*args, **kwargs))
        resp.content_type = "application/json"
        return resp
    return wrap

class Jobs(object):
    @classmethod
    def map(cls, map):
        print "S:", repr(cls), dir(cls)
        with map.submapper(controller=cls, path_prefix="/jobs") as m:
            m.connect('/next', method='next_job')
            m.connect('/run/{item}', method='run_job')
            m.connect('/complete/{item}', method='complete_job')
            m.connect('/{job_id}', method='get_job', conditions={"method": ["GET"]})
            m.connect('/', method='new_job', conditions={"method": ["POST"]})

    def get_job(self, req, job_id):
        #query = session.Query()
        pass
        
    @json_post
    def new_job(self, req, data):
        job_data = json.loads(req.body)

        pj = pbatch.model.Job() 
        pj.status = "pending"
        
        keys = ["uid", "gid", "user", "command", "args", "env",
                "stdin", "stdout", "stderr"]

        for k in keys:
            if k in job_data:
                setattr(pj, k, job_data[k])

        ret = session.add(pj)
        session.commit()

        return dict(pj)

    def next_job(self, req):
        return "NEXT JOB"

    def run_job(self, req, **kwargs):
        return "RUN JOB:" + repr(kwargs)

    def complete_job(self, req, **kwargs):
        return "COMP JOB"

Jobs.map(dispatcher.map)

session = None

def start_wsgiref():
    session = pbatch.model.connect()
    print "PB server."
    from wsgiref.util import setup_testing_defaults
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, dispatcher)
    print "Serving on port 8000..."
    httpd.serve_forever()

start = start_wsgiref
