# -*- coding: utf-8 -*-
"""Elasticsearch support for Bottle.

This module provides a Bottle extension for supporting Elasticsearch for:

    - injecting a Elasticsearch connection into handler functions

This module contains the following public classes:

    - ElasticPlugin -- The plugin for supporting handler functions.

"""
import elasticsearch

__all__ = ['ElasticPlugin', ]

import collections
import inspect

from bottle import PluginError


class ElasticPlugin(object):
    """Elasticsearch Plugin for Bottle.

    Connect to a elasticsearch cluster, and add a DB in a Bottle callback
    Sample :

        import bottle
        from bottle_es import ElasticPlugin

        app = bottle.Bottle()
        plugin = ElasticPlugin(hosts=["..."])
        app.install(plugin)

        @app.route('/')
        def show(elastic):
            response = ...
            # elastic see at: https://elasticsearch-py.readthedocs.org/
            return response

    hosts : nodes endpoint
    keyword : Override parameter name in Bottle function.

    This constructor passes any optional parameter to elasticsearch.ElasticSearch constructor.

    """
    name = 'elasticsearch'
    api = 2

    def __init__(self, hosts, keyword='elastic', *args, **kwargs):
        """

        :param hosts: list of nodes to connect
        :param keyword: parameter name in Bottle function
        :param args:
        :param kwargs:
        """
        if not isinstance(hosts, collections.Iterable):
            raise PluginError("Elasticsearch hosts is required")
        self.hosts = hosts
        self.conn = None
        self.keyword = keyword
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        """
        string representation
        :return:
        """
        return "bottle_es.ElasticPlugin(keyword=%r)" % (self.keyword)

    def __repr__(self):
        """
        string representation
        :return:
        """
        return "bottle_es.ElasticPlugin(keyword=%r)" % (self.keyword)

    def setup(self, app):
        """Called as soon as the plugin is installed to an application.
        :rtype: object
        """
        for other in app.plugins:
            if not isinstance(other, ElasticPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another Elastic plugin with conflicting settings (non-unique keyword).")

        if self.conn is None:
            self.conn = elasticsearch.Elasticsearch(hosts=self.hosts, **self.kwargs)

    def apply(self, callback, context):
        """Return a decorated route callback.
        :rtype: object
        """
        args = inspect.getargspec(context.callback)[0]
        # Skip this callback if we don't need to do anything
        if self.keyword not in args:
            return callback

        def wrapper(*a, **ka):
            ka[self.keyword] = self.conn
            rv = callback(*a, **ka)
            return rv

        return wrapper

    def close(self):
        if self.conn:
            self.conn = None
