#Submit and run
import argparse
#import optparse
import os
import sys
import json

import requests

from simplebatch.model import Job
import simplebatch.client

def run():
    print "prun"

def submit_main(args):
    parser = argparse.ArgumentParser(description='Submit a job to be run later')

    parser.add_argument('--stdin', action="store", dest="STDIN_FILE", type=str)
    parser.add_argument('--stdout', action="store", dest="STDOUT_FILE", default = '/dev/null', type=str)
    parser.add_argument('--strerr', action="store", dest="STDERR_FILE", default = '/dev/null', type=str)
    parser.add_argument('COMMAND')
    parser.add_argument('ARGS', nargs="+")
    
    options = parser.parse_args(args)
    #print "O:", options
    j = Job()
    #print os.environ
    j.stdin = options.STDIN_FILE
    j.stdout = options.STDOUT_FILE
    j.stderr = options.STDERR_FILE

    j.uid = os.getuid()
    j.gid = os.getgid()
    j.env = dict(os.environ)

    j.command = options.COMMAND
    j.args = options.ARGS

    r = simplebatch.client.submit_job(j)
    print "Queued job:", r['job_id']

def submit():
    submit_main(sys.argv[1:])
