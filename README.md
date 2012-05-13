pbatch
===

Simple Batch Processing

Daemons
===

pbatch
---

REST server keeps track of jobs.
Sooner:
/jobs           POST - create a new job
/jobs/id        
/jobs/next
/jobs/run       POST, mark a job as runnign
/jobs/complete  POST, mark a job as done

Later:
/jobs/pending   GET the collection
/jobs/running   
/jobs/completed 

pbatch_worker
---

Polls pbatch for a job.  If it is going to run it, it sends a starting call.

Tools
===

psub

pstatus

prun

pkill


TODO
===

Use built in sqlite3 for now.

Pending table
Running table
complete table
