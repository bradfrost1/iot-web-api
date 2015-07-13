from main import get_app
from api.database import client

from tornado import testing
from tornado.ioloop import IOLoop

import os
import json
import unittest


TEST_DB = 'test_iotapi'


class RestApiTestCase(testing.AsyncHTTPTestCase):
    def setUp(self):
        self.db = client[TEST_DB]
        super().setUp()

    def tearDown(self):
        client.drop_database(self.db)
        super().tearDown()

    def get_app(self):
        return get_app(db=self.db)

    def get_new_ioloop(self):
        "Syncs the test loop with motor client settin the IOLoop to a singleton"
        return IOLoop.instance()

    def test_send_data_to_an_entity(self):
        response = self.fetch('/data/for/my-device',
            method='POST', headers={
                'Content-Type': 'application/json'
            }, body="""{
                "temperature": 12,
                "status": "ok"
            }""")
        body = json.loads(response.body.decode('utf-8'))

        assert response.code == 201
        assert 'entity' in body
        assert 'created' in body
        assert 'content' in body

    @unittest.skip("TODO")
    def test_get_latest_data_from_entity(self):
        response = self.fetch('/get/data/from/my-device')
        body = json.loads(response.body.decode('utf-8'))

        assert 'results' in body
        assert len(body['results']) == 1

    @unittest.skip("TODO")
    def test_get_data_from_entity(self):
        response = self.fetch('/get/latest/data/from/my-device')
        body = json.loads(response.body.decode('utf-8'))

        assert 'results' in body
        assert len(body['results']) > 0

    @unittest.skip("TODO")
    def test_listen_data_from_entity(self):
        pass
