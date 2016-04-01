Bottle Elasticsearch
==============

.. image:: https://travis-ci.org/bsao/bottle-elastic.svg?branch=master
    :target: https://travis-ci.org/bsao/bottle-elastic

This bottle-elastic plugin integrates Elasticsearch with your Bottle
application. It injects a Elastic connection in your route and handle the
session cycle.

Support elasticsearch 2.x


Usage Example:

.. code-block:: python

    from bottle import Bottle
    from bottle_elastic import ElasticPlugin
    from datetime import datetime

    app = Bottle()
    plugin = ElasticPlugin(hosts=["localhost:9200"])
    app.install(plugin)

    @app.route('/', method='GET')
    def index(elastic):
        # elastic search operation
        return "ok"

    @app.route('/create/', method='POST')
    def create(elastic):
        doc = {
            'name': 'bsao',
            'text': 'Elasticsearch: cool.',
            'timestamp': datetime.now(),
        }
        response = elastic.index(index="test-index", doc_type='tweet', id=1, body=doc)
        return response

