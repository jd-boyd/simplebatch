import json

import webob
from webtest import TestApp

from pbatch.daemons import server

def eq(a, b):
    assert a == b, "Not equal: %s == %s" % (repr(a), repr(b))

def test_json_return():
    def test(method, args, kwargs, results):
        meth = server.json_return(method)
        eq(json.loads(meth(*args, **kwargs).body), results)
        
    def test_method1(arg):
        return "A"
    yield test, test_method1, [4], {}, "A"

    def test_method2(args={}):
        return {"A": args}
    yield test, test_method2, ["B"], {}, {"A": "B"}

def test_json_post():
    def test(method, args, results):
        meth = server.json_post(method)
        eq(json.loads(meth(*args).body), results)
        
    def test_method1(req, data):
        return "A"
    req = webob.Request({})
    req.body = '"A"'
    yield test, test_method1, [req], "A"

    def test_method2(self, req, data):
        return "A"
    req = webob.Request({})
    req.body = '"A"'
    yield test, test_method2, [{}, req], "A"

def test_new_job():
    app = TestApp(server.dispatcher)
    res = app.post_json("/jobs/", {"cli": "ls -l"}, status=200)
    eq(res.json, {"job_id": 1234}) 

def test_get_job():
    app = TestApp(server.dispatcher)
    res = app.get("/jobs/1234", status=200)
