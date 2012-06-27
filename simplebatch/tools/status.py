import argparse
import sys

import simplebatch.client

def status_main(args):
    parser = argparse.ArgumentParser(description='Show the status of jobs in the system.')

    parser.add_argument('--running', action="store_true", default=False)
    parser.add_argument('--pending', action="store_true", default = False)
    parser.add_argument('--complete', action="store_true", default =False)
    parser.add_argument('--killed', action="store_true", default =False)
    parser.add_argument('--all', action="store_true", default =False)

    options = parser.parse_args(args)

    # If all are false, set all to true so that all are done.
    o = filter(None, options.__dict__.values())
    if o==[]:
        options.__dict__['all'] = True

    print options

    all_jobs = simplebatch.client.get_all_jobs()

    def filt(job):
        if options.all:
            return True
        if options.running and job['status']=="running":
            return True
        if options.complete and job['status']=="complete":
            return True
        if options.pending and job['status']=="pending":
            return True
        if options.killed and job['status']=="killed":
            return True
        return False

        
    jobs_to_print = filter(filt, all_jobs)
    #TODO Filtering based on flags stuff.
    
    for job in jobs_to_print:
        print "ID: %4d" % job['job_id'], "Status: %9s" % job['status'], "CMD:", job['command']
    

def status():
    status_main(sys.argv[1:])

def kill():
    #TODO: switch to proper argparse
    simplebatch.client.kill_job(int(sys.argv[1]))
