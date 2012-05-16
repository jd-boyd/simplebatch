from webtest import TestApp

from pbatch.daemons import server

def eq(a, b, msg=""):
    assert a == b, msg

def test_json_return():
    pass

def test_new_job():
    app = TestApp(server.dispatcher)
    res = app.post_json("/jobs/", {"cli": "ls -l"}, status=200)
    eq(res.json, {"job_id": 1234}) 

def test_get_job():
    app = TestApp(server.dispatcher)
    res = app.get("/jobs/1234", status=200)
