from tornado.web import url, StaticFileHandler

from api.views import (
    PostDataHandler, GetDataHandler, ListenDataHandler, DataSocketHandler
)

import os


ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

urls = [
    url(r"/data/for/(.*)",              PostDataHandler),
    url(r"/get/data/from/(.*)",         GetDataHandler, dict(limit=100)),
    url(r"/get/latest/data/from/(.*)",  GetDataHandler, dict(limit=1)),
    url(r"/listen/data/from/(.*)",      ListenDataHandler),
    url(r"/socket/for/(.*)",            DataSocketHandler),
    url(r"/(.*)", StaticFileHandler, {
        'path': os.path.join(ROOT_PATH, 'static'),
        'default_filename': 'index.html',
    }),
]
