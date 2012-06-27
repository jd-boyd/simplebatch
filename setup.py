#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='simplebatch',
      version='1.0',
      description='Simple Batch Processing',
      author='Joshua D. Boyd',
      author_email='jdboyd@jdboyd.net',
      setup_requires=['nose'],
      install_requires=['sqlalchemy',
                        'argparse',
                        'WebOb',
                        'routes',
                        'requests'
                        ],
      tests_require=[
          'webtest',
          'mock'
      ],
      packages = find_packages(),
      entry_points = {'console_scripts': ['brun = simplebatch.tools.sub:run',
                                          'bsubmit = simplebatch.tools.sub:submit',
                                          'bkill = simplebatch.tools.status:kill',
                                          'bstatus = simplebatch.tools.status:status',
                                          'batchd = simplebatch.daemons.server:start',                                         
                                          'batch_worker = simplebatch.daemons.worker:start',                                         
                                          'batch_manager = simplebatch.daemons.manager:start',                                         
                                          ]}
     )
