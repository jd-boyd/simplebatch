import argparse
import sys

import pbatch.client

def status_main(args):
    parser = argparse.ArgumentParser(description='Show the status of jobs in the system.')

    parser.add_argument('--running', action="store_true", default=False)
    parser.add_argument('--pending', action="store_true", default = False)
    parser.add_argument('--complete', action="store_true", default =False)
    parser.add_argument('--killed', action="store_true", default =False)

    options = parser.parse_args(args)

    # If all are false, set all to true so that all are done.
    o = filter(None, options.__dict__.values())
    if o==[]:
        for k in options.__dict__:
            options.__dict__[k] = True

    print options

    if options.complete:
        pass

def status():
    status_main(sys.argv[1:])

def kill():
    #TODO: switch to proper argparse
    pbatch.client.kill_job(int(sys.argv[1]))
