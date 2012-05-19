import argparse
import json
import os
import datetime

import webob
from webob.dec import wsgify
import routes

import pbatch.model
from pbatch.daemons.wsgi_util import Dispatcher, json_post, json_return

dispatcher = Dispatcher()

class Jobs(object):
    @classmethod
    def map(cls, map):
        print "S:", repr(cls), dir(cls)
        with map.submapper(controller=cls, path_prefix="/jobs") as m:
            m.connect('/next', method='next_job')
            m.connect('/{job_id}/run', method='run_job')
            m.connect('/{job_id}/complete', method='complete_job')
            m.connect('/{job_id}', method='get_job', 
                      conditions={"method": ["GET"]})
            m.connect('/', method='new_job', conditions={"method": ["POST"]})

    @json_return
    def get_job(self, req, job_id):
        job = session.query(pbatch.model.Job).get(job_id)
        if job is None:
            raise webob.exc.HTTPNotFound()

        return job.toDict()        
        
    @json_post
    def new_job(self, req, post_data):
        job_data = post_data

        job = pbatch.model.Job() 
        job.status = "pending"
        
        keys = ["uid", "gid", "user", "command", "args", "env",
                "stdin", "stdout", "stderr"]

        for k in keys:
            if k in job_data:
                setattr(job, k, job_data[k])

        ret = session.add(job)
        session.commit()

        return job.toDict()

    def next_job(self, req):
        return "NEXT JOB"

    def run_job(self, req, job_id):
        job = session.query(pbatch.model.Job).get(job_id)
        if job is None:
            raise webob.exc.HTTPNotFound()

        #TODO: be sure status is pending.  If not return 403, with json error

        job.status="running"
        job.start_time = datetime.datetime.now()
        session.commit()

        raise webob.exc.HTTPTemporaryRedirect(location='/job/'+str(job_id))
        
    @json_post    
    def complete_job(self, req, job_id, post_data):
        job = session.query(pbatch.model.Job).get(job_id)
        if job is None:
            raise webob.exc.HTTPNotFound()

        #TODO: be sure status is running.  If not return 403, with json error

        job.status="complete"
        job.end_time = datetime.datetime.now()
        job.return_code = post_data['return_code']
        session.commit()

        raise webob.exc.HTTPTemporaryRedirect(location='/job/'+str(job_id))

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
