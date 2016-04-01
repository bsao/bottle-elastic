#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import bottle
import elasticsearch
from bottle import PluginError

from bottle_elastic import ElasticPlugin


class ElasticsearchPluginTest(unittest.TestCase):
    def test_with_keyword(self):
        app = bottle.Bottle(catchall=False)
        plugin = ElasticPlugin(hosts=['localhost'])
        app.install(plugin)

        @app.get('/')
        def test(elastic):
            self.assertEqual(type(elastic), type(elasticsearch.Elasticsearch()))
            self.assertTrue(elastic.transport.hosts == [{'host': 'localhost'}])

        app({'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

    def test_without_keyword(self):
        app = bottle.Bottle(catchall=False)
        plugin = ElasticPlugin(hosts=['localhost'])
        app.install(plugin=plugin)

        @app.get('/')
        def test():
            pass

        app({'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

        @app.get('/2')
        def test_kw(**kw):
            self.assertFalse('elastic' in kw)

        app({'PATH_INFO': '/2', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

        @app.get('/3')
        def test_kw(elastic):
            self.assertEqual(type(elastic), type(elasticsearch.Elasticsearch()))
            self.assertTrue(elastic.transport.hosts == [{'host': 'localhost'}])

        app({'PATH_INFO': '/3', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

    def test_client_string_param(self):
        app = bottle.Bottle(catchall=False)
        plugin = ElasticPlugin(hosts='localhost')
        app.install(plugin)

        @app.get('/')
        def test(elastic):
            self.assertEqual(type(elastic), type(elasticsearch.Elasticsearch()))
            self.assertTrue(elastic.transport.hosts == [{'host': 'localhost'}])

        app({'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

    def test_error_diferent_keyworks(self):
        app = bottle.Bottle(catchall=False)
        plugin = ElasticPlugin(hosts='localhost', keyword='es')
        app.install(plugin)

        @app.get('/')
        def test(elastic):
            self.assertEqual(type(elastic), type(elasticsearch.Elasticsearch()))
            self.assertTrue(elastic.transport.hosts == [{'host': 'localhost'}])

        with self.assertRaises(Exception):
            app({'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

    def test_error_duplicated_keyworks(self):
        with self.assertRaises(PluginError):
            app = bottle.Bottle(catchall=False)
            app.install(ElasticPlugin(hosts='localhost', keyword='es'))
            app.install(ElasticPlugin(hosts='localhost', keyword='es'))

    def test_client_list_param(self):
        app = bottle.Bottle(catchall=False)
        plugin = ElasticPlugin(hosts=['localhost', 'localhost1'])
        app.install(plugin)

        @app.get('/')
        def test(elastic):
            self.assertEqual(type(elastic), type(elasticsearch.Elasticsearch()))
            self.assertTrue(elastic.transport.hosts == [{'host': 'localhost'}, {'host': 'localhost1'}])

        app({'PATH_INFO': '/', 'REQUEST_METHOD': 'GET'}, lambda x, y: None)

    def test_invalid_hosts(self):
        with self.assertRaises(PluginError):
            ElasticPlugin(hosts=1)


if __name__ == '__main__':
    unittest.main()
