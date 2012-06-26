pbatch
===

Simple Batch Processing

Daemons
===

pbatchd
---

REST server keeps track of jobs.
Sooner:
/jobs           POST - create a new job, GET - get all jobs
/jobs/id        
/jobs/next
/jobs/id/run       POST, mark a job as running
/jobs/id/complete  POST, mark a job as done
/jobs/id/kill      POST, mark a job as killed

Later:
/jobs/pending   GET the collection
/jobs/running   
/jobs/completed 

pbatch_worker
---

Polls pbatch for a job.  If it is going to run it, it sends a starting call.

pbatch_manager
---

Manages a pool of workers.  This will be rolled into pbatchd eventually, but for now it is seperate to get the kinks worked out.

Tools
===

psubmit

pkill

later: 
pstatus

prun



TODO
===

Use built in sqlite3 for now.

Add actuall integration tests between client and server.

Add a -p flag to patchd to put pid in a file.

Supply initd, upstart, and SMF files.
