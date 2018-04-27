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
            if req.content_length:
                body = json.load(req.stream)
            exc = processor.process(cfg.get('processing', lower=True), body)
            resp.body = exc
            resp.status = falcon.HTTP_200
        except Exception as exc:
            logging.error('Server Error: %s', exc.message)
            logging.debug('Server Error: %s', exc.message, exc_info=1)
            resp.body = {"Sever Error": exc.message}
            resp.status = falcon.HTTP_500
        resp.body = json.dumps(resp.body)


DEBUG = cfg.get('http', lower=True).get('debug')
configure_base_logger(level='debug' if DEBUG else 'info')
api = application = falcon.API()
api.add_route('/', Ping())
api.add_route('/v{}'.format(__version__), Resource())
