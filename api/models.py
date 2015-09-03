from datetime import datetime, timedelta
from copy import copy
from tornado import gen


CONN_TIMEOUT = timedelta(seconds=1)


@gen.coroutine
def do_insert(entity, content):
    now = datetime.utcnow()
    obj = {
        'entity':   entity,
        'created':  now,
        'content':  self.json,
    }
    result = yield self.db.stream.insert(copy(obj))
    return obj


@gen.coroutine
def do_find(entity, limit=100):
    cursor = self.db.stream.find({'entity': entity}, {'_id': 0})\
        .sort('created', pymongo.DESCENDING)
    result = yield cursor.to_list(length=limit)
    return result


def get_tail_cursor(entity):
    now = datetime.datetime.utcnow()
    return self.db.stream.find({
            'entity': entity,
            'created': {
                '$gt': now,
            },
        }, {
            '_id': 0
        }, tailable=True, await_data=True)


@gen.coroutine
def do_tail(entity):
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
