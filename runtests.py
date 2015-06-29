import tornado.testing
import unittest
import os


def all():
    return unittest.defaultTestLoader.discover(os.path.dirname(__file__))


if __name__ == '__main__':
    tornado.testing.main()
