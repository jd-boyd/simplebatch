import argparse
import os

import webapp2

import pbatch.model

# class job(webapp2.RequestHandler):
#     def post(self, name):
#         # Create
#         if not name: 
#             name = 'World'
#         self.response.write('Hello, ' + name + '!')

#     def get(self, id):
#         print "GET JOB:", id

class next_job(webapp2.RequestHandler):
    def get(self):
        self.response.write("NEXT JOB")
        #Get the next job

# class run_job(webapp2.RequestHandler):
#     def post(self):
#         self.response.write("RUN JOB")
#         #get the next job

# class complete_job(webapp2.RequestHandler):
#     def post(self):
#         self.response.write("COMP JOB")
#         #get the next job

urls = [
    ('/jobs/next', next_job),
#    ('/jobs/run', run_job),
#    ('/jobs/complete', complete_job),
#    ('/jobs/([0-9]*)', job),
]
app = webapp2.WSGIApplication(urls, debug=True)

def start():
    print "PB server."
    app.run()
