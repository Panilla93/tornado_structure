#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson
from tornado import template

from config.config import DATABASE, PORT
import tornado.web
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
    def initialize(self, database, method):
        self.database = database
        self.method = method

    # RETURN __DOC__ METHOD
    def get(self):
        self.render("static/service.html", docs=inspect.getdoc(self.method))

    # RETURN VALUE METHOD
    def post(self):
        res = self.method(self.request)
        self.write(res)
        self.finish()


class ServiceApplication(tornado.web.Application):
    def __init__(self, db, **settings):
        handlers = []
        paths = {}
        for n_mod, path, method in PUBLIC_METHODS:
            self._to_dict(n_mod, paths, path)
            handlers.append(
                [path, BasicHandler, dict(database=db, method=method)])
        handlers.append(['/', InitHandler, dict(paths=paths)])
        settings = {"static_path": STATIC}
        super(ServiceApplication, self).__init__(handlers, **settings)

    def _to_dict(self, n_mod, paths, path):
        if n_mod in paths:
            paths[n_mod].append(path)
        else:
            paths[n_mod] = [path]


if __name__ == "__main__":
    database = DATABASE
    puerto = PORT

    ServiceApplication(database).listen(puerto)
    print("Start in: http://localhost:8888")
    tornado.ioloop.IOLoop.instance().start()
