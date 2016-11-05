#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT, PORT
import tornado.web
from peewee import PostgresqlDatabase
import importlib
import types
import inspect
import os

# PATHS
HOME = os.path.join(os.path.dirname(__file__))
STATIC = os.path.join(HOME, 'static')

PUBLIC_METHODS = []
PUBLIC_MODULES = ['users']

# To import the public methods
for n_mod in PUBLIC_MODULES:
    # Import the module
    try:
        mod = importlib.import_module('services.%s' % n_mod)

        # Each all the functions of the module
        for n_serv in dir(mod):
            serv = getattr(mod, n_serv)
            # Keep the necessary functions
            if isinstance(serv, types.FunctionType):
                PUBLIC_METHODS.append((n_mod, "/service/%s.py/%s" % (n_mod, n_serv), serv))
    except ImportError:
        pass


class InitHandler(tornado.web.RequestHandler):
    def initialize(self, paths):
        self.paths = paths

    def get(self):
        self.render("static/index.html", paths=self.paths)

class BasicHandler(tornado.web.RequestHandler):
    def initialize(self, method):
        self.method = method

    # RETURN __DOC__ METHOD
    def get(self):
        self.render("static/service.html", docs=inspect.getdoc(self.method))

    # RETURN VALUE METHOD
    def post(self):
        self.connection = PostgresqlDatabase(DB_NAME, user=DB_USER, port=DB_PORT,
                                             password=DB_PASSWORD, host=DB_HOST)
        res = self.method(self.request)
        self.write(res)
        self.finish()


class ServiceApplication(tornado.web.Application):
    def __init__(self, **settings):
        handlers = []
        paths = {}
        for n_mod, path, method in PUBLIC_METHODS:
            self._to_dict(n_mod, paths, path)
            handlers.append(
                [path, BasicHandler, dict(method=method)])
        handlers.append(['/', InitHandler, dict(paths=paths)])
        settings = {"static_path": STATIC}
        super(ServiceApplication, self).__init__(handlers, **settings)

    def _to_dict(self, n_mod, paths, path):
        if n_mod in paths:
            paths[n_mod].append(path)
        else:
            paths[n_mod] = [path]


if __name__ == "__main__":
    ServiceApplication().listen(PORT)
    print("Start in: http://localhost:8888")
    tornado.ioloop.IOLoop.instance().start()
