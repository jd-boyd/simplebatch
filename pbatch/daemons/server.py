import argparse
import os

#import webapp2
import webob
from webob.dec import wsgify

import routes

import pbatch.model

# class job(webapp2.RequestHandler):
#     def post(self, name):
#         # Create
#         if not name: 
#             name = 'World'
#         self.response.write('Hello, ' + name + '!')

#     def get(self, id):
#         print "GET JOB:", id

#class next_job(webapp2.RequestHandler):
#    def get(self):
class Jobs(object):
    @wsgify
    def next_job(self, req):
        return webob.Response("NEXT JOB")
        #Get the next job

# class run_job(webapp2.RequestHandler):
#     def post(self):
#         self.response.write("RUN JOB")
#         #get the next job

# class complete_job(webapp2.RequestHandler):
#     def post(self):
#         self.response.write("COMP JOB")
#         #get the next job

#urls = [
#    ('/jobs/next', next_job),
#    ('/jobs/run', run_job),
#    ('/jobs/complete', complete_job),
#    ('/jobs/([0-9]*)', job),
#]
#app = webapp2.WSGIApplication(urls, debug=True)

map = routes.Mapper()
map.connect('/jobs/next', view='jobs', method='next_job')
#map.connect('/view/{item}', view=view)

views = {"jobs": Jobs()}

class Dispatcher(object):
    @wsgify
    def __call__(self, req):
        results = map.routematch(environ=req.environ)
        if not results:
            return webob.exc.HTTPNotFound()
        match, route = results
        req.urlvars = ((), match)
        kwargs = match.copy()
        view = kwargs.pop('view')
        method = kwargs.pop('method')

        return getattr(views[view], method)(req, **kwargs)

def start():
    print "PB server."
    from wsgiref.util import setup_testing_defaults
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, Dispatcher())
    print "Serving on port 8000..."
    httpd.serve_forever()
