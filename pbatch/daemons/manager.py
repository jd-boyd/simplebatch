import os, sys
import argparse
import logging
import time

log = logging.getLogger(__name__)

WORKER_CNT = 2
WORKER = "/home/jdboyd/.virtualenvs/pbatch/bin/pbatch_worker"
stopping = False
workers = []

def make_worker():
    pid = os.fork()
    if pid == 0:
        print "This is the child"
        os.execv(WORKER, [WORKER])
    else:
        return pid


def main(args):
    parser = argparse.ArgumentParser(description='Run jobs int the queue')

    #parser.add_argument('--single', action="store_true", default=False)
    
    options = parser.parse_args(args)

    while not stopping:
        if len(workers) != WORKER_CNT:
            log.info
            new_worker = make_worker()
            workers.append(new_worker)
        else:
            pass

        for worker in workers:
            ret = os.waitpid(worker, os.WNOHANG)
            if ret != (0, 0):
                workers.remove(worker)
        time.sleep(5)


def start():
    """Entry point.  It just calls main with the CLI args to make it 
    easier to test."""
    main(sys.argv[1:])

