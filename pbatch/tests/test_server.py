import re

from nose.plugins.skip import Skip, SkipTest
import webob
from webtest import TestApp

from pbatch.daemons import server

from pbatch.tests.util import eq

class TestClass(object):
    def setUp(self):
#        import sys
#        sys.stderr.write("Setup")
        server.session = server.pbatch.model.connect("sqlite://")

    def tearDown(self):
        server.session = None

    def test_new_job(self):
        app = TestApp(server.dispatcher)
        res = app.post_json("/jobs/", {"cli": "ls -l", 'env': ''}, status=200)
        eq(res.json['job_id'], 1)
        eq(res.json['status'], "pending")

        res = app.post_json("/jobs/", {"cli": "df", 'env': ''}, status=200)
        eq(res.json['job_id'], 2)
        eq(res.json['status'], "pending")

    def test_get_job(self):
        app = TestApp(server.dispatcher)

        res = app.post_json("/jobs/", {"cli": "ls -l", 'env': ''}, status=200)
        job_id = res.json['job_id']

        res = app.get("/jobs/1", status=200)
        eq(res.json['job_id'], 1)
        eq(res.json['status'], "pending")

    def test_get_job(self):
        app = TestApp(server.dispatcher)
        res = app.get("/jobs/1234", status=404)

    def test_run_job_not_found(self):
        app = TestApp(server.dispatcher)
        res = app.post_json("/jobs/1234/run", {}, status=404)

    def test_run_job(self):
        app = TestApp(server.dispatcher)

        res = app.post_json("/jobs/", {"cli": "ls -l", 'env': ''}, status=200)
        job_id = res.json['job_id']

        res = app.post_json("/jobs/1/run", {}, status=307)

        res = app.get("/jobs/1", status=200)
        eq(res.json['job_id'], 1)
        eq(res.json['status'], "running")
        assert re.match("^[1-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]T[0-9][0-9][0-9][0-9][0-9][0-9]$", res.json['start_time']), res.json['start_time']

    def test_complete_job_not_found(self):
        app = TestApp(server.dispatcher)
        res = app.post_json("/jobs/1234/complete", {"return_code": 4040}, status=404)

    def test_complete_job(self):
        app = TestApp(server.dispatcher)

        res = app.post_json("/jobs/", {"cli": "ls -l", 'env': ''}, status=200)
        job_id = res.json['job_id']

        res = app.post_json("/jobs/1/run", {}, status=307)

        res = app.post_json("/jobs/1/complete", {"return_code": 42}, status=307)

        res = app.get("/jobs/1", status=200)
        eq(res.json['job_id'], 1)
        eq(res.json['status'], "complete")
        eq(res.json['return_code'], 42)
        assert re.match("^[1-9][0-9][0-9][0-9][0-1][0-9][0-3][0-9]T[0-9][0-9][0-9][0-9][0-9][0-9]$", res.json['end_time']), res.json['end_time']
        assert res.json['end_time'] >= res.json['start_time']

    def test_complete_job_without_running(self):
        raise SkipTest()
        app = TestApp(server.dispatcher)

        res = app.post_json("/jobs/", {"cli": "ls -l", 'env': ''}, status=200)
        job_id = res.json['job_id']

        res = app.post_json("/jobs/1/complete", {"return_code": 42}, status=307)
        assert False
