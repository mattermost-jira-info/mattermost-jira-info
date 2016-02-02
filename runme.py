#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import wsgi
from tornado import httpserver
from tornado import ioloop

import hook

http_server = httpserver.HTTPServer(wsgi.WSGIContainer(hook.app))
http_server.listen(5000)
ioloop.IOLoop.instance().start()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
