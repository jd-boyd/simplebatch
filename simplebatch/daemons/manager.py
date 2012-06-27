import os, sys
import argparse
import logging
import time

log = logging.getLogger(__name__)

WORKER_CNT = detectCPUs()
WORKER = "/home/jdboyd/.virtualenvs/simplebatch/bin/batch_worker"
stopping = False
workers = []

def make_worker():
    pid = os.fork()
    if pid == 0:
        print "This is the child"
        os.execv(WORKER, [WORKER])
    else:
        return pid


# lifted from: http://codeliberates.blogspot.com/2008/05/detecting-cpuscores-in-python.html
def detectCPUs():
    """
    Detects the number of CPUs on a system. Cribbed from pp.
    """
    # Linux, Unix and MacOS:
    if hasattr(os, "sysconf"):
        if os.sysconf_names.has_key("SC_NPROCESSORS_ONLN"):
            # Linux & Unix:
            ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
            if isinstance(ncpus, int) and ncpus > 0:
                return ncpus
        else: # OSX:
            return int(os.popen2("sysctl -n hw.ncpu")[1].read())
     # Windows:
        if os.environ.has_key("NUMBER_OF_PROCESSORS"):
            ncpus = int(os.environ["NUMBER_OF_PROCESSORS"]);
            if ncpus > 0:
                return ncpus
    return 1 # Default

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

