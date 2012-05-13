#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pbatch',
      version='1.0',
      description='Simple Batch Processing',
      author='Joshua D. Boyd',
      author_email='jdboyd@jdboyd.net',
      packages = find_packages(),
      entry_points = {'console_scripts': ['prun = pbatch.tools.sub:run',
                                          'psubmit = pbatch.tools.sub:submit',
                                          'pkill = pbatch.tools.status:kill',
                                          'pstatus = pbatch.tools.status:status',
                                          'pbatchd = pbatch.daemons.server:start',                                         
                                          'pbatch_worker = pbatch.daemons.worker:start',                                         
                                          ]}
     )
