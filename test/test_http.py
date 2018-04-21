
import falcon
from falcon import testing
import pytest

from processing import __version__
from processing.http import api


@pytest.fixture
def client():
    return testing.TestClient(api)


def tests_ping(client):
    response = client.simulate_get('/')
    assert response.status == falcon.HTTP_OK
    assert response.content.startswith('This is an ESPA processing node')

def tests_post(client):
    response = client.simulate_get('/v{}'.format(__version__))
    assert response.status == falcon.HTTP_405
