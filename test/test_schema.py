
import pytest
import marshmallow

from processing import schema

@pytest.fixture
def base_order():
    return {
        'input_name': 'LT04_L1TP_030031_19890420_20161002_01_T1',
        'input_urls': [],
        'metadata': {'order_id': 'this-orderid'},
        'products': [ 'toa_refl' ],
        }

def test_not_valid_id(base_order):
    base_order.update({'input_name': 'not_valid'})
    with pytest.raises(marshmallow.ValidationError):
        assert {} != schema.load(base_order)


def test_base_schema_missing(base_order):
    _ = base_order.pop('metadata')
    with pytest.raises(marshmallow.ValidationError):
        assert {} != schema.load(base_order)


def test_base_schema(base_order):
    assert base_order == schema.load(base_order)


def test_extents_missing_minx(base_order):
    base_order.update({
        'customization': {'output_format': 'envi'},
        'extents': {'maxx': '2.0'},
    })
    with pytest.raises(marshmallow.ValidationError):
        assert {} != schema.load(base_order)


@pytest.fixture
def extents_options(base_order):
    base_order.update({
        'customization': {'output_format': 'envi'},
        'extents': {
            'minx': '1.0',
            'maxx': '2.0',
            'miny': '1.0',
            'maxy': '2.0',
            },
    })
    return base_order


def test_extents_missing(extents_options):
    extents_options['extents'].pop('maxx')
    with pytest.raises(marshmallow.ValidationError):
        assert {} != schema.load(extents_options)


def test_extents_valid(extents_options):
    assert {} != schema.load(extents_options)


@pytest.fixture
def sinu_proj_opts(base_order):
    base_order.update({
        'customization': {'output_format': 'envi'},
        'projection': {'sinu': {
            'central_meridian': '-96.0',
            'false_easting': '2.0',
            'false_northing': '2.0',
        }}
    })
    return base_order


def test_sinu_missing(sinu_proj_opts):
    sinu_proj_opts['projection']['sinu'].pop('central_meridian')
    with pytest.raises(marshmallow.ValidationError):
        assert {} != schema.load(sinu_proj_opts)


def test_sinu_valid(sinu_proj_opts):
    assert {} != schema.load(sinu_proj_opts)


@pytest.fixture
def aea_proj_opts(base_order):
    base_order.update({
        'customization': {'output_format': 'envi'},
        'projection': {'aea': {
            'central_meridian': '-96.0',
            'std_parallel_1': '29.0',
            'std_parallel_2': '70.0',
            'origin_latitude': '40.0',
            'false_easting': '2.0',
            'false_northing': '2.0',
            'datum': 'wgs84',
        }}
    })
    return base_order


def test_aea_missing(aea_proj_opts):
    aea_proj_opts['projection']['aea'].pop('origin_latitude')
    with pytest.raises(marshmallow.ValidationError):
        assert {} != schema.load(aea_proj_opts)


def test_aea_valid(aea_proj_opts):
    assert {} != schema.load(aea_proj_opts)


@pytest.fixture
def utm_proj_opts(base_order):
    base_order.update({
        'customization': {'output_format': 'envi'},
        'projection': {'utm': {
            'utm_zone': '10',
            'utm_north_south': 'north',
        }}
    })
    return base_order


def test_utm_missing(utm_proj_opts):
    utm_proj_opts['projection']['utm'].pop('utm_zone')
    with pytest.raises(marshmallow.ValidationError):
        assert {} != schema.load(utm_proj_opts)


def test_utm_valid(utm_proj_opts):
    assert {} != schema.load(utm_proj_opts)


@pytest.fixture
def ps_projection(base_order):
    base_order.update({
        'customization': {'output_format': 'envi'},
        'projection': {'ps': {
            'utm_zone': '10',
            'latitude_true_scale': '-90.0',
            'longitude_pole': '0.0',
            'origin_latitude': '-90.0',
            'false_easting': '2.0',
            'false_northing': '2.0',
        }}
    })
    return base_order


def test_ps_missing(ps_projection):
    ps_projection['projection']['ps'].pop('latitude_true_scale')
    with pytest.raises(marshmallow.ValidationError):
        assert {} != schema.load(ps_projection)


def test_ps_valid(ps_projection):
    assert {} != schema.load(ps_projection)
