import json

from requests import Request
from mock import patch, MagicMock

import pbatch.client
from pbatch.model import Job
from pbatch.tests.util import eq

class TestObj(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            setattr(self, k, v)

def test_submit_job():
    j = Job()
    t = TestObj(json={'job_id': 1})
    mock = MagicMock(return_value = t)
    with patch('pbatch.client.requests.post', mock):
        r = pbatch.client.submit_job(j)
        print "R:", r
        eq(r['job_id'], 1)

    job_dict = j.toDict()
    del job_dict['status']
    del job_dict['job_id']
    del job_dict['start_time']
    del job_dict['end_time']
    mock.assert_called_with('http://localhost:8000/jobs/', data=json.dumps(job_dict),
                      headers={'content-type': 'application/json'})

def test_mark_job_running():
    t = TestObj(json={'job_id': 1})
    mock = MagicMock(return_value = t)
    with patch('pbatch.client.requests.post', mock):
        r = pbatch.client.mark_job_running(1)
        print "R:", r
        eq(r['job_id'], 1)
    
    mock.assert_called_with('http://localhost:8000/jobs/1/run', data=json.dumps({}), headers={'content-type': 'application/json'})

def test_mark_job_complete():
    t = TestObj(json={'job_id': 1})
    mock = MagicMock(return_value = t)
    with patch('pbatch.client.requests.post', mock):
        r = pbatch.client.mark_job_complete(1, 42)
        print "R:", r
        eq(r['job_id'], 1)
    
    mock.assert_called_with('http://localhost:8000/jobs/1/complete', data=json.dumps({'return_code': 42}), headers={'content-type': 'application/json'})

def test_get_job():
    t = TestObj(json={'job_id': 1})
    mock = MagicMock(return_value = t)
    with patch('pbatch.client.requests.get', mock):
        r = pbatch.client.get_job(1)
        print "R:", r
        eq(r['job_id'], 1)
    
    mock.assert_called_with('http://localhost:8000/jobs/1')

def test_get_next_job():
    t = TestObj(json={'job_id': 1})
    mock = MagicMock(return_value = t)
    with patch('pbatch.client.requests.get', mock):
        r = pbatch.client.get_next_job()
        print "R:", r
        eq(r['job_id'], 1)
    
    mock.assert_called_with('http://localhost:8000/jobs/next')

def test_kill_job():
    t = TestObj(json={'job_id': 1})
    mock = MagicMock(return_value = t)
    with patch('pbatch.client.requests.post', mock):
        r = pbatch.client.kill_job(1)
        print "R:", r
        eq(r['job_id'], 1)
    
    mock.assert_called_with('http://localhost:8000/jobs/1/kill', data=json.dumps({}), headers={'content-type': 'application/json'})

