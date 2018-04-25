""" HTTP transport layer """
import logging
import json

import falcon

import cfg
import processor
from utilities import configure_base_logger
from . import __version__


class Ping(object):
    def on_get(self, req, resp):
        resp.body = 'This is an ESPA processing node'
        resp.status = falcon.HTTP_200


class Resource(object):
    def on_post(self, req, resp):
        try:
            resp.body = processor.process(cfg, req)
            resp.status = falcon.HTTP_200
        except Exception as exc:
            logging.error('Server Error: %s', exc.message)
            resp.body = {"Sever Error": exc.message}
            resp.status = falcon.HTTP_500
        resp.body = json.dumps(resp.body)


configure_base_logger(level='debug' if cfg.get('http').get('debug') else 'info')
api = application = falcon.API()
api.add_route('/', Ping())
api.add_route('/v{}'.format(__version__), Resource())
