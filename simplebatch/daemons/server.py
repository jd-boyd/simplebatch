import argparse
import json
import os
import datetime
import logging

import webob
from webob.dec import wsgify
import routes

import simplebatch.model
from simplebatch.model import Job
from sqlalchemy import or_

from simplebatch.daemons.wsgi_util import Dispatcher, json_post, json_return

dispatcher = Dispatcher()

log = logging.getLogger(__name__)

class Jobs(object):
    @classmethod
    def map(cls, map):
        print "S:", repr(cls), dir(cls)
        with map.submapper(controller=cls, path_prefix="/jobs") as m:
            m.connect('/next', method='next_job')
            m.connect('/{job_id}/run', method='run_job')
            m.connect('/{job_id}/kill', method='kill_job')
            m.connect('/{job_id}/complete', method='complete_job')
            m.connect('/{job_id}', method='get_job', 
                      conditions={"method": ["GET"]})
            m.connect('/', method='new_job', conditions={"method": ["POST"]})
            m.connect('/', method='all_jobs', conditions={"method": ["GET"]})

    @json_return
    def get_job(self, req, job_id):
        job = session.query(Job).get(job_id)
        if job is None:
            raise webob.exc.HTTPNotFound()

        ret_job = job.toDict()        
        ret_job['env'] = json.loads(job.env)
        ret_job['args'] = json.loads(job.args)
        return ret_job
        
    @json_post
    def new_job(self, req, post_data):
        job_data = post_data

        job = Job() 
        job.status = "pending"
        
        keys = ["uid", "gid", "user", "command", "args", "env",
                "stdin", "stdout", "stderr"]

        for k in keys:
            if k in job_data:
                setattr(job, k, job_data[k])

        job.env = json.dumps(job_data.get('env', {}))
        job.args = json.dumps(job_data.get('args', []))

        ret = session.add(job)
        session.commit()

        return job.toDict()

    def next_job(self, req):
        job = session.query(Job.job_id, Job.status).order_by(Job.job_id).filter_by(status="pending").first()
        
        if job is None:
            raise webob.exc.HTTPNotFound()

        raise webob.exc.HTTPTemporaryRedirect(location='/jobs/'+str(job.job_id))

    @json_post
    def run_job(self, req, job_id, post_data):
        job = session.query(Job).get(job_id)
        if job is None:
            raise webob.exc.HTTPNotFound()
        
        filter_d = {"job_id": job_id,
                    "status": "pending"}
        
        update_fields = {Job.status: "running",
                         Job.start_time: datetime.datetime.now()
                         }
        ret = session.query(Job).filter_by(**filter_d).update(update_fields)
        session.commit()
        print "RET:", repr(ret)

        if ret==0:
            # Since we established that the job existed, if no rows were
            # updated, the job must not have been in the pending state.
            raise webob.exc.HTTPForbidden("Can only run pending jobs.")

        raise webob.exc.HTTPTemporaryRedirect(location='/job/'+str(job_id))
        
    @json_post    
    def complete_job(self, req, job_id, post_data):
        job = session.query(Job).get(job_id)
        if job is None:
            raise webob.exc.HTTPNotFound()
        
        filter_d = {"job_id": job_id,
                    "status": "running"}
        
        update_fields = {Job.status: "complete",
                         Job.end_time: datetime.datetime.now(),
                         Job.return_code: post_data['return_code']
                         }
        ret = session.query(Job).filter_by(**filter_d).update(update_fields)
        session.commit()
        print "RET:", repr(ret)

        if ret==0:
            # Since we established that the job existed, if no rows were
            # updated, the job must not have been in the pending state.
            raise webob.exc.HTTPForbidden("Can only run pending jobs.")

        raise webob.exc.HTTPTemporaryRedirect(location='/job/'+str(job_id))

    @json_post
    def kill_job(self, req, job_id, post_data):
        print "KILL JOB"
        job = session.query(Job).get(job_id)
        if job is None:
            print "Reject"
            raise webob.exc.HTTPNotFound()
        
        filter_d = {"job_id": job_id,
                    "status": "pending"}
        
        update_fields = {Job.status: "killed"}
        ret = session.query(Job).filter_by(**filter_d).update(update_fields)
        session.commit()
        print "RET:", repr(ret)

        if ret==0:
            # Since we established that the job existed, if no rows were
            # updated, the job must not have been in the pending state.
            raise webob.exc.HTTPForbidden("Can only delete pending jobs.")

        raise webob.exc.HTTPTemporaryRedirect(location='/job/'+str(job_id))

    @json_return
    def all_jobs(self, req):
        jobs = []
        ret = session.query(Job).order_by(Job.job_id)
        for job in ret:
            jobs.append( job.toDict() )
        return jobs

Jobs.map(dispatcher.map)

session = None

def start_wsgiref():
    global session
    session = simplebatch.model.connect()
    print "PB server:", session
    from wsgiref.util import setup_testing_defaults
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, dispatcher)
    print "Serving on port 8000..."
    httpd.serve_forever()

def start():

start = start_wsgiref
