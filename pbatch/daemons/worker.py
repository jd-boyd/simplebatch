import os
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
    full_cmd = [j['command']] + j['args']
    
    with open(j['stdin']) as stdin_fh, \
         open(j['stdout'], "w") as stdout_fh, \
         open(j['stderr'], "w") as stderr_fh:
         ret = subprocess.call(full_cmd, stdout=stdout_fh, 
                               stderr=stderr_fh, stdin=stdin_fh)
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
        for k in j['env']:
            os.environ[k] = j['env'][k]
        run_job(j)
        print 'CD'

def start():
    r = requests.get("http://localhost:8000/jobs/next")
    fork_job(r.json)

if __name__=="__main__":
    start()
