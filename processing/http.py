""" HTTP transport layer """

import falcon

import cfg
import processor
from . import __version__


class Ping(object):
    def on_get(self, req, resp):
        resp.body = 'This is an ESPA processing node'
        resp.status = falcon.HTTP_200


class Resource(object):
    def on_post(self, req, resp):
        return processor.get_instance(cfg.get('default'), req)


api = application = falcon.API()
api.add_route('/', Ping())
api.add_route('/v{}'.format(__version__), Resource())
