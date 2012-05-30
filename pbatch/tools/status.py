import argparse
import sys

import pbatch.client

def status():
    pass

def kill():
    pbatch.client.kill_job(int(sys.argv[1]))
