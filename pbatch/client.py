import json

import requests

from pbatch.model import Job

def submit_job(job):
    job_dict = job.toDict()
    drop_keys = ['job_id', 'status', 'end_time', 'start_time']
    for drop in drop_keys:
        del job_dict[drop]
    #print "DICT:", json.dumps(job_dict, indent=2)

    r = requests.post('http://localhost:8000/jobs/', data=json.dumps(job_dict),
                      headers={'content-type': 'application/json'})

    return r

def mark_job_running(job):
    job_dict = job.toDict()
    drop_keys = ['job_id', 'status', 'end_time', 'start_time']
    for drop in drop_keys:
        del job_dict[drop]
    #print "DICT:", json.dumps(job_dict, indent=2)

    r = requests.post('http://localhost:8000/jobs/', data=json.dumps(job_dict),
                      headers={'content-type': 'application/json'})

    return r

def mark_job_complete(job_id, ret):
    r = requests.post("http://localhost:8000/jobs/%d/complete" % job_id,
                      headers = {'content-type': 'application/json'},
                      data=json.dumps({"return_code": ret}))

    return r.json

def get_job(job_id):
    r = requests.get("http://localhost:8000/jobs/" + str(job_id))
    j = Job(r.json)
    return j

def get_next_job():
    r = requests.get("http://localhost:8000/jobs/next")
    j = Job(r.json)
    return j

    
