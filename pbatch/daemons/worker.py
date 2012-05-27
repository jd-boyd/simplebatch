import os
import json
import subprocess
import requests

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
    if j['args']:
        full_cmd +=  j['args']
    
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

    try:
        ret = subprocess.call(full_cmd, **opts)
    finally:
        if 'stdin' in opts:
            opts['stdin'].close()
        if 'stdout' in opts:
            opts['stdout'].close()
        if 'stderr' in opts:
            opts['stderr'].close()


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
        os.setgid(j['gid'])
        os.setuid(j['uid'])
        print "ENV:", repr(j['env'])
        if j['env']:
            for k in j['env']:
                os.environ[k] = j['env'][k]
        run_job(j)
        print 'CD'

def start():
    r = requests.get("http://localhost:8000/jobs/next")
    fork_job(r.json)

if __name__=="__main__":
    start()
