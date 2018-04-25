#!/usr/bin/env python

import pytest
import marshmallow

from processing import cli


def test_reconstruct_schema():
    expected = {'here': {'there': 1}}
    assert expected == cli.reconstruct_schema({'hello': 1}, {'here': {'there': 'hello'}})


def test_clear_all_none():
    expected = {'a': 1}
    assert expected == cli.clear_all_none({'a': 1, 'b': {'c': None}})


@pytest.fixture(scope="module")
def parser():
    return cli.build_command_line_parser()

@pytest.fixture(scope='function')
def options():
    return ['--order-id', 'ORDERID',
            '--input-product-id', 'LT04_L1TP_030031_19890420_20161002_01_T1',
            '--input-url', 'file://',]


def test_extents_missing_minx(parser, options):
    options.extend(['--product-type', 'landsat'])
    options.extend(['--output-format', 'envi'])
    options.extend(['--extent-maxx', '2.0'])

    with pytest.raises(marshmallow.ValidationError):
        args = cli.stack_args(vars(parser.parse_args(options)))

@pytest.fixture
def extents_options(options):
    options.extend(['--product-type', 'landsat'])
    options.extend(['--output-format', 'envi'])
    options.extend(['--extent-minx', '1.0'])
    options.extend(['--extent-maxx', '2.0'])
    options.extend(['--extent-miny', '1.0'])
    options.extend(['--extent-maxy', '2.0'])
    return options


def test_extents_missing(parser, extents_options):
    ix = extents_options.index('--extent-maxx')
    _ = extents_options.pop(ix), extents_options.pop(ix)
    with pytest.raises(marshmallow.ValidationError):
        args = cli.stack_args(vars(parser.parse_args(extents_options)))

def test_extents_valid(parser, extents_options):
    assert {} != cli.stack_args(vars(parser.parse_args(extents_options)))


@pytest.fixture
def sinu_proj_opts(options):
    options.extend(['--product-type', 'landsat'])
    options.extend(['--output-format', 'envi'])
    options.extend(['--target-projection', 'sinu'])
    options.extend(['--central-meridian', '-96.0'])
    options.extend(['--false-easting', '2.0'])
    options.extend(['--false-northing', '2.0'])
    return options

def test_sinu_missing(parser, sinu_proj_opts):
    ix = sinu_proj_opts.index('--central-meridian')
    _ = sinu_proj_opts.pop(ix), sinu_proj_opts.pop(ix)
    with pytest.raises(marshmallow.ValidationError):
        args = cli.stack_args(vars(parser.parse_args(sinu_proj_opts)))

def test_sinu_valid(parser, sinu_proj_opts):
    assert {} != cli.stack_args(vars(parser.parse_args(sinu_proj_opts)))


@pytest.fixture
def aea_proj_opts(options):
    options.extend(['--product-type', 'landsat'])
    options.extend(['--output-format', 'envi'])
    options.extend(['--target-projection', 'aea'])
    options.extend(['--central-meridian', '-96.0'])
    options.extend(['--std-parallel-1', '29.0'])
    options.extend(['--std-parallel-2', '70.0'])
    options.extend(['--origin-latitude', '40.0'])
    options.extend(['--false-easting', '2.0'])
    options.extend(['--false-northing', '2.0'])
    options.extend(['--datum', 'wgs84'])
    return options

def test_aea_missing(parser, aea_proj_opts):
    ix = aea_proj_opts.index('--origin-latitude')
    _ = aea_proj_opts.pop(ix), aea_proj_opts.pop(ix)
    with pytest.raises(marshmallow.ValidationError):
        args = cli.stack_args(vars(parser.parse_args(aea_proj_opts)))

def test_aea_valid(parser, aea_proj_opts):
    assert {} != cli.stack_args(vars(parser.parse_args(aea_proj_opts)))


@pytest.fixture
def utm_proj_opts(options):
    options.extend(['--product-type', 'landsat'])
    options.extend(['--output-format', 'envi'])
    options.extend(['--target-projection', 'utm'])
    options.extend(['--utm-zone', '10'])
    options.extend(['--utm-north-south', 'north'])
    return options

def test_utm_missing(parser, utm_proj_opts):
    ix = utm_proj_opts.index('--utm-zone')
    _ = utm_proj_opts.pop(ix), utm_proj_opts.pop(ix)
    with pytest.raises(marshmallow.ValidationError):
        args = cli.stack_args(vars(parser.parse_args(utm_proj_opts)))

def test_utm_valid(parser, utm_proj_opts):
    assert {} != cli.stack_args(vars(parser.parse_args(utm_proj_opts)))


@pytest.fixture
def ps_projection(options):
    options.extend(['--product-type', 'landsat'])
    options.extend(['--output-format', 'envi'])
    options.extend(['--target-projection', 'ps'])
    options.extend(['--latitude-true-scale', '-90.0'])
    options.extend(['--longitude-pole', '0.0'])
    options.extend(['--origin-latitude', '-90.0'])
    options.extend(['--false-easting', '2.0'])
    options.extend(['--false-northing', '2.0'])
    return options

def test_ps_missing(parser, ps_projection):
    ix = ps_projection.index('--latitude-true-scale')
    _ = ps_projection.pop(ix), ps_projection.pop(ix)
    with pytest.raises(marshmallow.ValidationError):
        args = cli.stack_args(vars(parser.parse_args(ps_projection)))

def test_ps_valid(parser, ps_projection):
    assert {} != cli.stack_args(vars(parser.parse_args(ps_projection)))
