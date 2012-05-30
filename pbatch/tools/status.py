import argparse
import sys

import pbatch.client

def status_main(args):
    parser = argparse.ArgumentParser(description='Submit a job to be run later')

    parser.add_argument('--running', action="store_true", default=False)
    parser.add_argument('--pending', action="store_true", default = False)
    parser.add_argument('--complete', action="store_true", default =False)
    parser.add_argument('--killed', action="store_true", default =False)

    parser.add_argument('ARGS', nargs="+")
    
    options = parser.parse_args(args)

    print options

def status():
    status_main(sys.argv[1:])

def kill():
    #TODO: switch to proper argparse
    pbatch.client.kill_job(int(sys.argv[1]))
