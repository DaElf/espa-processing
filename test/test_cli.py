#!/usr/bin/env python

import pytest

from processing import cli


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

    def test_load_template(self):
        import os
        print(os.getcwd())
        print('$'*25)
        cli.load_template('processing/order_template.json')
        with pytest.raises(cli.BadTemplateError):
            cli.load_template('test/test-orders/empty.json')
        with pytest.raises(ValueError):
            cli.load_template('test/test-orders/garbage.json')

    def test_extents_not_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])

        args = parser.parse_args(options)
        assert not cli.check_for_extents(args)

    def test_extents_missing_minx(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--extent-maxx', '2.0'])
        with pytest.raises(cli.MissingExtentError):
            args = parser.parse_args(options)
            cli.check_for_extents(args)

    def test_extents_missing_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--extent-minx', '1.0'])

        # Missing maxx
        with pytest.raises(cli.MissingExtentError):
            args = parser.parse_args(options)
            cli.check_for_extents(args)

        # Missing miny
        options.extend(['--extent-maxx', '2.0'])
        with pytest.raises(cli.MissingExtentError):
            args = parser.parse_args(options)
            cli.check_for_extents(args)

        # Missing maxy
        options.extend(['--extent-miny', '1.0'])
        with pytest.raises(cli.MissingExtentError):
            args = parser.parse_args(options)
            cli.check_for_extents(args)

        # Check all options
        options.extend(['--extent-maxy', '2.0'])

        args = parser.parse_args(options)
        assert cli.check_for_extents(args)

    def test_not_sinu_specified(self, parser, options):
        # Check not sinu
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'utm'])

        args = parser.parse_args(options)
        assert not cli.check_projection_sinu(args)

    def test_sinu_specified(self, parser, options):
        # Check missing options
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])

        # Missing central meridian
        with pytest.raises(cli.MissingSinuError):
            args = parser.parse_args(options)
            cli.check_projection_sinu(args)

        # Missing false easting
        options.extend(['--central-meridian', '-96.0'])
        with pytest.raises(cli.MissingSinuError):
            args = parser.parse_args(options)
            cli.check_projection_sinu(args)

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        with pytest.raises(cli.MissingSinuError):
            args = parser.parse_args(options)
            cli.check_projection_sinu(args)

        # Check all options
        options.extend(['--false-northing', '2.0'])

        args = parser.parse_args(options)
        assert cli.check_projection_sinu(args)

    def test_not_aea_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'sinu'])

        args = parser.parse_args(options)
        assert not cli.check_projection_aea(args)
        assert not cli.check_projection_utm(args)
        assert not cli.check_projection_ps(args)

    def test_aea_specified(self, parser, options):
        # Check missing options
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'aea'])

        # Missing central meridian
        with pytest.raises(cli.MissingAeaError):
            args = parser.parse_args(options)
            cli.check_projection_aea(args)

        # Missing std parallel 1
        options.extend(['--central-meridian', '-96.0'])
        with pytest.raises(cli.MissingAeaError):
            args = parser.parse_args(options)
            cli.check_projection_aea(args)

        # Missing std parallel 2
        options.extend(['--std-parallel-1', '29.0'])
        with pytest.raises(cli.MissingAeaError):
            args = parser.parse_args(options)
            cli.check_projection_aea(args)

        # Missing origin latitude
        options.extend(['--std-parallel-2', '70.0'])
        with pytest.raises(cli.MissingAeaError):
            args = parser.parse_args(options)
            cli.check_projection_aea(args)

        # Missing false easting
        options.extend(['--origin-latitude', '40.0'])
        with pytest.raises(cli.MissingAeaError):
            args = parser.parse_args(options)
            cli.check_projection_aea(args)

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        with pytest.raises(cli.MissingAeaError):
            args = parser.parse_args(options)
            cli.check_projection_aea(args)

        # Missing datum
        options.extend(['--false-northing', '2.0'])
        with pytest.raises(cli.MissingAeaError):
            args = parser.parse_args(options)
            cli.check_projection_aea(args)

        # Check all options
        options.extend(['--datum', 'wgs84'])

        args = parser.parse_args(options)
        assert cli.check_projection_aea(args)

    def test_utm_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'utm'])

        # Missing utm zone
        with pytest.raises(cli.MissingUtmError):
            args = parser.parse_args(options)
            cli.check_projection_utm(args)

        # Missing utm north south
        options.extend(['--utm-zone', '10.0'])
        with pytest.raises(cli.MissingUtmError):
            args = parser.parse_args(options)
            cli.check_projection_utm(args)

        # Check all options
        options.extend(['--utm-north-south', 'north'])

        args = parser.parse_args(options)
        assert cli.check_projection_utm(args)

    def test_ps_specified(self, parser, options):
        options.extend(['--product-type', 'landsat'])
        options.extend(['--output-format', 'envi'])
        options.extend(['--target-projection', 'ps'])

        # Missing latitude true scale
        with pytest.raises(cli.MissingPsError):
            args = parser.parse_args(options)
            cli.check_projection_ps(args)

        # Missing longitude pole
        options.extend(['--latitude-true-scale', '-90.0'])
        with pytest.raises(cli.MissingPsError):
            args = parser.parse_args(options)
            cli.check_projection_ps(args)

        # Missing origin latitude
        options.extend(['--longitude-pole', '0.0'])
        with pytest.raises(cli.MissingPsError):
            args = parser.parse_args(options)
            cli.check_projection_ps(args)

        # Missing false easting
        options.extend(['--origin-latitude', '-71.0'])
        with pytest.raises(cli.MissingPsError):
            args = parser.parse_args(options)
            cli.check_projection_ps(args)

        # Missing false northing
        options.extend(['--false-easting', '2.0'])
        with pytest.raises(cli.MissingPsError):
            args = parser.parse_args(options)
            cli.check_projection_ps(args)

        # Check all options
        options.extend(['--false-northing', '2.0'])

        args = parser.parse_args(options)
        assert cli.check_projection_ps(args)
