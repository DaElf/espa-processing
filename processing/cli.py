#! /usr/bin/env python
'ESPA Processing Command Line Interface'

from argparse import ArgumentParser
import logging

import cfg
import processor
from utilities import configure_base_logger
from schema import ProcessingRequestSchema

from . import __version__


def build_command_line_parser():
    """Builds the command line parser

    Returns:
        <parser>: Command line parser
    """

    parser = ArgumentParser(description=__doc__)

    parser.add_argument('--version',
                        action='version',
                        version=__version__)

    # ------------------------------------------------------------------------
    specific = parser.add_argument_group('order specifics')

    specific.add_argument('--order-id',
                          action='store',
                          dest='order_id',
                          required=True,
                          metavar='TEXT',
                          help='Order ID')

    specific.add_argument('--input-product-id',
                          action='store',
                          dest='product_id',
                          required=True,
                          metavar='TEXT',
                          help='Input Product ID')

    specific.add_argument('--product-type',
                          action='store',
                          dest='product_type',
                          required=True,
                          choices=['landsat', 'modis', 'plot'],
                          help='Type of product we are producing')

    specific.add_argument('--input-url',
                          action='store',
                          dest='input_url',
                          required=True,
                          metavar='TEXT',
                          nargs='+',
                          help=('Complete URL path to the input product.'
                                '  Supported ("file://...", "http://...")'))

    specific.add_argument('--espa-api',
                          action='store',
                          dest='espa_api',
                          required=False, # TODO: REMOVE THIS
                          metavar='TEXT',
                          help='URL for the ESPA API')

    specific.add_argument('--output-format',
                          action='store',
                          dest='output_format',
                          required=False,
                          choices=['envi', 'gtiff', 'hdf-eos2', 'netcdf'],
                          help='Output format for the product')

    specific.add_argument('--work-dir',
                          action='store',
                          dest='work_dir',
                          required=False, # TODO: REMOVE THIS
                          metavar='TEXT',
                          help='Base processing directory')

    specific.add_argument('--dist-method',
                          action='store',
                          dest='dist_method',
                          required=False, # TODO: REMOVE THIS
                          choices=['local', 'remote'],
                          metavar='TEXT',
                          help='Distribution method')

    specific.add_argument('--dist-dir',
                          action='store',
                          dest='dist_dir',
                          required=False, # TODO: REMOVE THIS
                          metavar='TEXT',
                          help='Distribution directory')

    specific.add_argument('--bridge-mode',
                          action='store_true',
                          dest='bridge_mode',
                          help='Specify bridge processing mode')

    # ------------------------------------------------------------------------
    products = parser.add_argument_group('products')

    products.add_argument('--include-pixel-qa',
                          action='store_true',
                          dest='include_pixel_qa',
                          help='Include PixelQA Products')

    products.add_argument('--include-customized-source-data',
                          action='store_true',
                          dest='include_customized_source_data',
                          help='Include Customized Source Data')

    products.add_argument('--include-surface-temperature',
                          action='store_true',
                          dest='include_st',
                          help='Include Surface Temperature')

    products.add_argument('--include-surface-reflectance',
                          action='store_true',
                          dest='include_sr',
                          help='Include Surface Reflectance')

    products.add_argument('--include-sr-evi',
                          action='store_true',
                          dest='include_sr_evi',
                          help='Include Surface Reflectance based EVI')

    products.add_argument('--include-sr-msavi',
                          action='store_true',
                          dest='include_sr_msavi',
                          help='Include Surface Reflectance based MSAVI')

    products.add_argument('--include-sr-nbr',
                          action='store_true',
                          dest='include_sr_nbr',
                          help='Include Surface Reflectance based NBR')

    products.add_argument('--include-sr-nbr2',
                          action='store_true',
                          dest='include_sr_nbr2',
                          help='Include Surface Reflectance based NBR2')

    products.add_argument('--include-sr-ndmi',
                          action='store_true',
                          dest='include_sr_ndmi',
                          help='Include Surface Reflectance based NDMI')

    products.add_argument('--include-sr-ndvi',
                          action='store_true',
                          dest='include_sr_ndvi',
                          help='Include Surface Reflectance based NDVI')

    products.add_argument('--include-sr-savi',
                          action='store_true',
                          dest='include_sr_savi',
                          help='Include Surface Reflectance based SAVI')

    products.add_argument('--include-top-of-atmosphere',
                          action='store_true',
                          dest='include_toa',
                          help='Include Top-of-Atmosphere Reflectance')

    products.add_argument('--include-brightness-temperature',
                          action='store_true',
                          dest='include_brightness_temperature',
                          help='Include Thermal Brightness Temperature')

    products.add_argument('--include-surface-water-extent',
                          action='store_true',
                          dest='include_surface_water_extent',
                          help='Include Surface Water Extent')

    products.add_argument('--include-statistics',
                          action='store_true',
                          dest='include_statistics',
                          help='Include Statistics')

    # ------------------------------------------------------------------------
    custom = parser.add_argument_group('customization')

    custom.add_argument('--resample-method',
                        action='store',
                        dest='resample_method',
                        choices=['near', 'bilinear', 'cubic',
                                 'cubicspline', 'lanczos'],
                        help='Resampling method to use')

    custom.add_argument('--pixel-size',
                        action='store',
                        dest='pixel_size',
                        metavar='FLOAT',
                        type=float,
                        help='Pixel size for the output product')

    custom.add_argument('--pixel-size-units',
                        action='store',
                        dest='pixel_size_units',
                        choices=['meters', 'dd'],
                        help='Units for the pixel size')

    custom.add_argument('--extent-units',
                        action='store',
                        dest='extent_units',
                        choices=['meters', 'dd'],
                        help='Units for the extent')

    custom.add_argument('--extent-minx',
                        action='store',
                        dest='extent_minx',
                        metavar='FLOAT',
                        type=float,
                        help='Minimum X direction extent value')

    custom.add_argument('--extent-maxx',
                        action='store',
                        dest='extent_maxx',
                        metavar='FLOAT',
                        type=float,
                        help='Maximum X direction extent value')

    custom.add_argument('--extent-miny',
                        action='store',
                        dest='extent_miny',
                        metavar='FLOAT',
                        type=float,
                        help='Minimum Y direction extent value')

    custom.add_argument('--extent-maxy',
                        action='store',
                        dest='extent_maxy',
                        metavar='FLOAT',
                        type=float,
                        help='Maximum Y direction extent value')

    custom.add_argument('--target-projection',
                        action='store',
                        dest='target_projection',
                        choices=['sinu', 'aea', 'utm', 'ps', 'lonlat'],
                        help='Reproject to this projection')

    custom.add_argument('--false-easting',
                        action='store',
                        dest='false_easting',
                        metavar='FLOAT',
                        type=float,
                        help='False Easting reprojection value')

    custom.add_argument('--false-northing',
                        action='store',
                        dest='false_northing',
                        metavar='FLOAT',
                        type=float,
                        help='False Northing reprojection value')

    custom.add_argument('--datum',
                        action='store',
                        dest='datum',
                        choices=['wgs84', 'nad27', 'nad83'],
                        help='Datum to use during reprojection')

    custom.add_argument('--utm-north-south',
                        action='store',
                        dest='utm_north_south',
                        choices=['north', 'south'],
                        help='UTM North or South')

    custom.add_argument('--utm-zone',
                        action='store',
                        dest='utm_zone',
                        metavar='INT',
                        type=int,
                        help='UTM Zone reprojection value')

    custom.add_argument('--central-meridian',
                        action='store',
                        dest='central_meridian',
                        metavar='FLOAT',
                        type=float,
                        help='Central Meridian reprojection value')

    custom.add_argument('--latitude-true-scale',
                        action='store',
                        dest='latitude_true_scale',
                        metavar='FLOAT',
                        type=float,
                        help='Latitude True Scale reprojection value')

    custom.add_argument('--longitude-pole',
                        action='store',
                        dest='longitude_pole',
                        metavar='FLOAT',
                        type=float,
                        help='Longitude Pole reprojection value')

    custom.add_argument('--origin-latitude',
                        action='store',
                        dest='origin_latitude',
                        metavar='FLOAT',
                        type=float,
                        help='Origin Latitude reprojection value')

    custom.add_argument('--std-parallel-1',
                        action='store',
                        dest='std_parallel_1',
                        metavar='FLOAT',
                        type=float,
                        help='Standard Parallel 1 reprojection value')

    custom.add_argument('--std-parallel-2',
                        action='store',
                        dest='std_parallel_2',
                        metavar='FLOAT',
                        type=float,
                        help='Standard Parallel 2 reprojection value')

    # ------------------------------------------------------------------------
    developer = parser.add_argument_group('developer')

    developer.add_argument('--dev-mode',
                           action='store_true',
                           dest='dev_mode',
                           help='Specify developer mode')

    developer.add_argument('--dev-intermediate',
                           action='store_true',
                           dest='dev_intermediate',
                           help='Specify keeping intermediate data files')

    developer.add_argument('--debug',
                           action='store_true',
                           dest='debug',
                           help='Specify debug logging')

    return parser


def reconstruct_schema(args, mapping):
    """ Convert flat argument set to nested schema

    Args:
        args (dict): key/value pairs supplied in flat format
        mapping (dict): schema tree where strings become args

    Returns:
        dict: nested schema populated from args

    Example:
        >>> reconstruct_schema({'hello': 1}, {'here': {'there': 'hello'}})
        {'here': {'there': 1}}
    """
    return {k: (args[v] if isinstance(v, str)
                else reconstruct_schema(args, v))
            for k, v in mapping.items() }


def clear_all_none(args):
    """ Strip all None from a key/value structure, including keys which nested them

    Args:
        args (dict): key/value pairs which may contain None values

    Returns:
        dict: structure with all None removed and no empty values

    Example:
        >>> clear_all_none({'a': 1, 'b': {'c': None}})
        {'a': 1}
    """
    return dict((x, y) for x, y in [
                (k, (v if not isinstance(v, dict) else clear_all_none(v)))
                for k, v in args.items() if v is not None ] if y != {})


def stack_args(cli_args):
    """ Converts the flat processing options into nested JSON

    Args:
        cli_args (dict): arguments parsed from the CLI

    Returns:
        dict: nested dictionary grouped by types/usage
    """
    # TODO: this function is not very flexible... :`(
    CLI_TO_SCHEMA = {
        'input_name': 'product_id',
        'input_urls': 'input_url',
        'metadata': {
            'orderid': 'order_id'
        },
        'options': {
            'customization': {
                'output_format': 'output_format',
                'resample_method': 'resample_method',
                'pixel_size': 'pixel_size',
                'pixel_size_units': 'pixel_size_units',
            },
            'extents': {
                'image_extents_units': 'extent_units',
                'minx': 'extent_minx',
                'maxx': 'extent_maxx',
                'miny': 'extent_miny',
                'maxy': 'extent_maxy',
            }
        }
    }
    nested_args = reconstruct_schema(cli_args, CLI_TO_SCHEMA)

    nested_args['options']['projection'] = dict()
    nested_args['options']['projection'][cli_args['target_projection']] = dict()
    projection = nested_args['options']['projection'][cli_args['target_projection']]
    PROJECTION_SCHEMA = {
        'false_easting': 'false_easting',
        'false_northing': 'false_northing',
        'datum': 'datum',
        'utm_north_south': 'utm_north_south',
        'utm_zone': 'utm_zone',
        'central_meridian': 'central_meridian',
        'latitude_true_scale': 'latitude_true_scale',
        'longitude_pole': 'longitude_pole',
        'origin_lat': 'origin_latitude',
        'std_parallel_1': 'std_parallel_1',
        'std_parallel_2': 'std_parallel_2',
    }
    projection.update(reconstruct_schema(cli_args, PROJECTION_SCHEMA))
    nested_args = clear_all_none(nested_args)
    return ProcessingRequestSchema().load(nested_args)


def parse_command_line():
    """Parses the command line

    Returns:
        dict: Command line arguments
    """
    parser = build_command_line_parser()
    args = vars(parser.parse_args())
    logging.debug('CLI Arguments: {}'.format(args))
    return args


def main():
    """ Command line entrypoint to process an order (stage, run, distrbute)
    """
    cli_args = stack_args(parse_command_line())
    configure_base_logger(level='debug' if cli_args.get('debug') else 'info')
    processor.process(cfg.get('processing'), cli_args)
