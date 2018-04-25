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
                      '--input-product-id', 'PRODUCT_ID',
                      '--input-url', 'file://',
                      '--espa-api', 'skip_api',
                      '--work-dir', '.',
                      '--dist-method', 'local',
                      '--dist-dir', '.']


class TestCLI(object):
    """Test the cli.py methods"""

    def test_extents_not_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])

        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

    def test_extents_missing_minx(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--extent-maxx', '2.0'])

        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

    def test_extents_missing_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--extent-minx', '1.0'])

        # Missing maxx
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing miny
        options.extend(['--extent-maxx', '2.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing maxy
        options.extend(['--extent-miny', '1.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Check all options
        options.extend(['--extent-maxy', '2.0'])

        assert parser.parse_args(options)


    def test_sinu_specified(self, parser, options):
        # Check missing options
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])

        # Missing central meridian
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing false easting
        options.extend(['--central-meridian', '-96.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Check all options
        options.extend(['--false-northing', '2.0'])

        assert parser.parse_args(options)

    def test_aea_specified(self, parser, options):
        # Check missing options
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'aea'])

        # Missing central meridian
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing std parallel 1
        options.extend(['--central-meridian', '-96.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing std parallel 2
        options.extend(['--std-parallel-1', '29.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing origin latitude
        options.extend(['--std-parallel-2', '70.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing false easting
        options.extend(['--origin-latitude', '40.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing datum
        options.extend(['--false-northing', '2.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Check all options
        options.extend(['--datum', 'wgs84'])

        assert parser.parse_args(options)

    def test_utm_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'utm'])

        # Missing utm zone
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing utm north south
        options.extend(['--utm-zone', '10.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Check all options
        options.extend(['--utm-north-south', 'north'])

        assert parser.parse_args(options)

    def test_ps_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'ps'])

        # Missing latitude true scale
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing longitude pole
        options.extend(['--latitude-true-scale', '-90.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing origin latitude
        options.extend(['--longitude-pole', '0.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing false easting
        options.extend(['--origin-latitude', '-71.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        with pytest.raises(marshmallow.ValidationError):
            args = parser.parse_args(options)

        # Check all options
        options.extend(['--false-northing', '2.0'])

        assert parser.parse_args(options)
