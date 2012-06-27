simplebatch
===

Simple Batch Processing

Daemons
===

batchd
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

batch_worker
---

Polls batchd for a job.  If it is going to run it, it sends a starting call.

batch_manager
---

Manages a pool of workers.  This will be rolled into batchd eventually,
but for now it is seperate to get the kinks worked out. 

Tools
===

bsubmit

bkill

later: 
bstatus

brun



TODO
===

Use built in sqlite3 for now.

Add actuall integration tests between client and server.

Add a -p flag to patchd to put pid in a file.

Supply initd, upstart, and SMF files.

Add a workers flag instead of just detecting.

Add slave mode to batchd.

Add any arguments to batchd
