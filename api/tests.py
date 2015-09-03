from main import get_app
from api.database import get_db_conn

from tornado import testing
from tornado.gen import Return
from tornado.ioloop import IOLoop
from tornado.concurrent import Future

import os
import json
import unittest
import unittest.mock as mock


TEST_DB = 'test_iotapi'

def mock_future(*args, **kwargs):
    yield Return(*args, **kwargs)


class RestApiTestCase(testing.AsyncHTTPTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @mock.patch('motor.MotorClient', autospec=True)
    def get_app(self, motor_client_mock):
        return get_app()


    @mock.patch('api.models.do_insert')
    def test_send_data_to_an_entity(self, do_insert_mock):
        # stream.insert.return_value = Return(True)
        print(do_insert_mock.call_count)

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
