import json

import webob
from webtest import TestApp

from pbatch.tests.util import eq

from pbatch.daemons import wsgi_util

def test_json_return():
    def test(method, args, kwargs, results):
        meth = wsgi_util.json_return(method)
        eq(json.loads(meth(*args, **kwargs).body), results)
        
    def test_method1(arg):
        return "A"
    yield test, test_method1, [4], {}, "A"

    def test_method2(args={}):
        return {"A": args}
    yield test, test_method2, ["B"], {}, {"A": "B"}

def test_json_post():
    def test(method, args, results):
        meth = wsgi_util.json_post(method)
        eq(json.loads(meth(*args).body), results)
        
    def test_method1(req, post_data):
        return "A"
    req = webob.Request({})
    req.body = '"A"'
    yield test, test_method1, [req], "A"

    def test_method2(self, req, post_data):
        return "A"
    req = webob.Request({})
    req.body = '"A"'
    yield test, test_method2, [{}, req], "A"

    def test_method3(self, req, job_id, post_data):
        assert type(post_data) is dict
        eq(post_data['return_code'], 42)
        eq(job_id, 1234)
        return "C"
    req = webob.Request({})
    req.body = '{"return_code": 42}'
    yield test, test_method3, [{}, req, 1234], "C"
