import os
import json

from api.routes import urls
from api.database import db
from api.utils import JSONEncoder, JSONDecoder

from tornado.ioloop import IOLoop
from tornado.web import Application

def get_app(**kwargs):
    options = {
        'db': db,
        'debug': True,
        'xsrf_cookies': False,
    }
    options.update(kwargs)
    return Application(urls, **options)


# Override default JSON behaviour
json._default_encoder = JSONEncoder()
json._default_decoder = JSONDecoder()


if __name__ == "__main__":
    import tornado.options
    tornado.options.parse_command_line()

    get_app().listen(8000)
    IOLoop.current().start()
