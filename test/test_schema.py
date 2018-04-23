
import pytest
import marshmallow

from processing import sensor
from processing import schema

@pytest.fixture
def base_order():
    return {
        'input_name': 'LT04_L1TP_030031_19890420_20161002_01_T1',
        'input_urls': [],
        'metadata': {'orderid': 'this-orderid'},
        'options': {}
        }

def test_not_valid_id(base_order):
    base_order.update({'input_name': 'not_valid'})
    with pytest.raises(sensor.ProductNotImplemented):
        schema.ProcessingRequestSchema().load(base_order)


def test_base_schema_missing(base_order):
    _ = base_order.pop('options')
    with pytest.raises(marshmallow.ValidationError):
        schema.ProcessingRequestSchema().load(base_order)


def test_base_schema(base_order):
    assert base_order == schema.ProcessingRequestSchema().load(base_order)

