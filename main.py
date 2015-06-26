import os
import json

from api.routes import urls
from api.database import db
from api.utils import JSONEncoder, JSONDecoder

from tornado.ioloop import IOLoop
from tornado.web import Application


app = Application(urls,
    db=db,
    debug=True,
    xsrf_cookies=False,)


# Override default JSON behaviour
json._default_encoder = JSONEncoder()
json._default_decoder = JSONDecoder()


if __name__ == "__main__":
    import tornado.options
    tornado.options.parse_command_line()

    app.listen(8000)
    IOLoop.current().start()
