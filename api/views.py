from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, asynchronous
from tornado.websocket import WebSocketHandler
from tornado import gen

import datetime
import json
import logging
import pymongo


CONN_TIMEOUT = datetime.timedelta(seconds=1)


class PostDataHandler(RequestHandler):
    JSON_TYPE = "application/json"

    def parse_json(self):
        if not self.request.body:
            self.json = {}
            return

        try:
            self.json = json.loads(self.request.body.decode('utf-8'))

        except ValueError as e:
            self.set_status(400)
            self.write({
                'error': "Invalid JSON: %s" % str(e)
            })
            self.finish()

    def prepare(self):
        content_type = self.request.headers.get('Content-Type', self.JSON_TYPE)

        if content_type.startswith(self.JSON_TYPE):
            self.parse_json()

        else:
            self.set_status(406)
            self.write({
                'error': "Only %s request are acceptable" % self.JSON_TYPE,
            })
            self.finish()

    def initialize(self):
        self.db = self.settings['db']

    @gen.coroutine
    def post(self, entity):
        now = datetime.datetime.utcnow()
        result = yield self.db.stream.insert({
            'entity':   entity,
            'created':  now,
            'content':  self.json,
        })

        self.set_status(201)
        self.write({
            'entity':   entity,
            'created':  now,
            'content':  self.json,
        })


class GetDataHandler(RequestHandler):
    def initialize(self, limit):
        self.db = self.settings['db']
        self.limit = limit

    @gen.coroutine
    def get(self, entity):
        cursor = self.db.stream.find({'entity': entity}, {'_id': 0})\
            .sort('created', pymongo.DESCENDING)
        result = yield cursor.to_list(length=self.limit)

        if len(result) == 0:
            self.set_status(404)
            self.write({
                'error': "Not found"
            })

        else:
            self.write({'results': result})


class ListenDataHandler(RequestHandler):
    def get_cursor_for(self, entity):
        now = datetime.datetime.utcnow()
        return self.db.stream.find(
            {
                'entity': entity,
                'created': {
                    '$gt': now,
                },
            }, {
                '_id': 0
            },
            tailable=True,
            await_data=True)

    def initialize(self):
        self.db = self.settings['db']

    def prepare(self):
        self.set_header('Connection', 'keep-alive')

    @asynchronous
    @gen.coroutine
    def get(self, entity):
        self.cursor = self.get_cursor_for(entity)

        while True:
            if self._finished:
                break

            if not self.cursor.alive:
                now = datetime.datetime.utcnow()
                # While collection is empty, tailable self.cursor dies immediately
                yield gen.Task(IOLoop.current().add_timeout, CONN_TIMEOUT)
                self.cursor = self.get_cursor_for(entity)

            if (yield self.cursor.fetch_next):
                result = self.cursor.next_object()

                self.write(result)
                yield self.flush()

    def on_connection_close(self):
        self.cursor.close()
        self.finish()


class DataSocketHandler(WebSocketHandler):
    def get_cursor_for(self, entity):
        now = datetime.datetime.utcnow()
        return self.db.stream.find(
            {
                'entity': entity,
                'created': {
                    '$gt': now,
                },
            }, {
                '_id': 0
            },
            tailable=True,
            await_data=True)

    def start_tail(self):
        # Create a permanente connection with the database
        while True:
            if not self.cursor.alive:
                now = datetime.datetime.utcnow()
                # While collection is empty, tailable self.cursor dies immediately
                yield gen.Task(IOLoop.current().add_timeout, CONN_TIMEOUT)
                self.cursor = self.get_cursor_for(entity)

            if (yield self.cursor.fetch_next):
                result = self.cursor.next_object()
                self.write_message(result)

    def check_origin(self, origin):
        "Allows cross-origin connections"
        return True

    def initialize(self):
        self.db = self.settings['db']

    @gen.coroutine
    def open(self, entity):
        self.entity = entity

        # Send the lastest data
        result = self.db.stream.find_one({'entity': entity}, {'_id': 0},
                sort=[('created', pymongo.DESCENDING)])

        if (yield result):
            self.write_message(result)
            start_tail()

        else:
            self.close(1003, "Not found")

    def on_message(self, message):
        now = datetime.datetime.utcnow()

        try:
            json = json.loads(self.request.body.decode('utf-8'))
            # Insert at database
            now = datetime.datetime.utcnow()
            result = yield self.db.stream.insert({
                'entity':   self.entity,
                'created':  now,
                'content':  json,
            })
            # Write output
            self.write_message({
                'entity':   self.entity,
                'content':  json,
                'created':  now,
            })

        except ValueError as e:
            self.write_message({
                'error': "Invalid JSON: %s" % str(e)
            })

    def on_close(self):
        if getattr(self, 'cursor', None):
            self.cursor.close()
