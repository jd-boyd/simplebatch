import os
import sys
import subprocess
import time
import argparse

import pbatch.client

# Get job
# Fork
# run job

fake_job = {
    'stdin': "/dev/zero",
    'stdout': "/tmp/stdout",
    'stderr': "/tmp/stderr",
    
    'uid': 1000,
    'gid': 1000,
    'env': {},
    
    'command': 'ls',
    'args': ['-l']
}

def run_job(j):
    full_cmd = [j['command']] 
    if j.args:
        full_cmd +=  j.args
    
    def setup_file(j, std):
        modes = {'stdin': "r",
                 'stdout': "w",
                 'stderr': "w"}
        ret = {}
        if j[std]:
            fh = open(j[std], modes[std])
        #BUG: Handle file couldn't be opened
            ret[std]=fh
        return ret

    opts = {}
    opts.update(setup_file(j, 'stdin'))
    opts.update(setup_file(j, 'stdout'))
    opts.update(setup_file(j, 'stderr'))

    pbatch.client.mark_job_running(j.job_id)
    try:
        ret = subprocess.call(full_cmd, **opts)
    finally:
        if 'stdin' in opts:
            opts['stdin'].close()
        if 'stdout' in opts:
            opts['stdout'].close()
        if 'stderr' in opts:
            opts['stderr'].close()

    pbatch.client.mark_job_complete(j.job_id, ret)

    return ret

def fork_job(j):
    pid = os.fork()
    if pid:
    #parent
        print "P:" 
        os.waitpid(pid, 0)
        print 'PD'
    else:
        print "C:"
        os.setgid(j.gid)
        os.setuid(j.uid)
        #print "ENV:", repr(j.env)
        if j.env:
            for k in j.env:
                os.environ[k] = j.env[k]
        run_job(j)
        print 'CD'



def main(args):
    parser = argparse.ArgumentParser(description='Run jobs int the queue')

    parser.add_argument('--single', action="store_true", default=False)
    
    options = parser.parse_args(args)

    loop = True

    while loop:
        job = pbatch.client.get_next_job()
        if job:
            print "Running job:", job.job_id
            fork_job(job)
        else:
            print "Got no job."
            time.sleep(10)

        if options.single:
            loop=False

def start():
    """Entry point.  It just calls main with the CLI args to make it 
    easier to test."""
    main(sys.argv[1:])
    
if __name__=="__main__":
    start()
