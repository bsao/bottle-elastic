#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import unittest

import bottle
import elasticsearch

from bottle_elastic import ElasticPlugin

py = sys.version_info
py3k = py >= (3, 0, 0)


class RedisTest(unittest.TestCase):
    def setUp(self):
        self.app = bottle.Bottle(catchall=False)

    def test_with_keyword(self):
        plugin = ElasticPlugin(hosts=['localhost'])
        self.plugin = self.app.install(plugin)

        @self.app.get('/')
        def test(elastic):
            self.assertEqual(type(elastic), type(elasticsearch.Elasticsearch()))

        self.app({'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

    def test_without_keyword(self):
        plugin = ElasticPlugin(hosts=['localhost'])
        self.plugin = self.app.install(plugin=plugin)

        @self.app.get('/')
        def test():
            pass

        self.app({'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

        @self.app.get('/2')
        def test_kw(**kw):
            self.assertFalse('elastic' in kw)

        self.app({'PATH_INFO': '/2', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)


if __name__ == '__main__':
    unittest.main()
