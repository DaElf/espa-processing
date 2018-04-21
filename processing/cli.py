#! /usr/bin/env python
'ESPA Processing Command Line Interface'

from argparse import ArgumentParser
import logging

import cfg
from logging_tools import configure_base_logger
import processor

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
                          help=('Complete URL path to the input product.'
                                '  Supported ("file://...", "http://...")'))

    specific.add_argument('--espa-api',
                          action='store',
                          dest='espa_api',
                          required=False,
                          metavar='TEXT',
                          default='skip_api',
                          help='URL for the ESPA API')

    specific.add_argument('--output-format',
                          action='store',
                          dest='output_format',
                          required=False,
                          choices=['envi', 'gtiff', 'hdf-eos2', 'netcdf'],
                          default='envi',
                          help='Output format for the product')

    specific.add_argument('--work-dir',
                          action='store',
                          dest='work_dir',
                          required=False,
                          default=None,
                          metavar='TEXT',
                          help='Base processing directory')

    specific.add_argument('--dist-method',
                          action='store',
                          dest='dist_method',
                          required=False,
                          choices=['local', 'remote'],
                          default='local',
                          metavar='TEXT',
                          help='Distribution method')

    specific.add_argument('--dist-dir',
                          action='store',
                          dest='dist_dir',
                          required=False,
                          default=None,
                          metavar='TEXT',
                          help='Distribution directory')

    specific.add_argument('--bridge-mode',
                          action='store_true',
                          dest='bridge_mode',
                          default=False,
                          help='Specify bridge processing mode')

    # ------------------------------------------------------------------------
    products = parser.add_argument_group('products')

    products.add_argument('--include-pixel-qa',
                          action='store_true',
                          dest='include_pixel_qa',
                          default=False,
                          help='Include PixelQA Products')

    products.add_argument('--include-customized-source-data',
                          action='store_true',
                          dest='include_customized_source_data',
                          default=False,
                          help='Include Customized Source Data')

    products.add_argument('--include-surface-temperature',
                          action='store_true',
                          dest='include_st',
                          default=False,
                          help='Include Surface Temperature')

    products.add_argument('--include-surface-reflectance',
                          action='store_true',
                          dest='include_sr',
                          default=False,
                          help='Include Surface Reflectance')

    products.add_argument('--include-sr-evi',
                          action='store_true',
                          dest='include_sr_evi',
                          default=False,
                          help='Include Surface Reflectance based EVI')

    products.add_argument('--include-sr-msavi',
                          action='store_true',
                          dest='include_sr_msavi',
                          default=False,
                          help='Include Surface Reflectance based MSAVI')

    products.add_argument('--include-sr-nbr',
                          action='store_true',
                          dest='include_sr_nbr',
                          default=False,
                          help='Include Surface Reflectance based NBR')

    products.add_argument('--include-sr-nbr2',
                          action='store_true',
                          dest='include_sr_nbr2',
                          default=False,
                          help='Include Surface Reflectance based NBR2')

    products.add_argument('--include-sr-ndmi',
                          action='store_true',
                          dest='include_sr_ndmi',
                          default=False,
                          help='Include Surface Reflectance based NDMI')

    products.add_argument('--include-sr-ndvi',
                          action='store_true',
                          dest='include_sr_ndvi',
                          default=False,
                          help='Include Surface Reflectance based NDVI')

    products.add_argument('--include-sr-savi',
                          action='store_true',
                          dest='include_sr_savi',
                          default=False,
                          help='Include Surface Reflectance based SAVI')

    products.add_argument('--include-top-of-atmosphere',
                          action='store_true',
                          dest='include_toa',
                          default=False,
                          help='Include Top-of-Atmosphere Reflectance')

    products.add_argument('--include-brightness-temperature',
                          action='store_true',
                          dest='include_brightness_temperature',
                          default=False,
                          help='Include Thermal Brightness Temperature')

    products.add_argument('--include-surface-water-extent',
                          action='store_true',
                          dest='include_surface_water_extent',
                          default=False,
                          help='Include Surface Water Extent')

    products.add_argument('--include-statistics',
                          action='store_true',
                          dest='include_statistics',
                          default=False,
                          help='Include Statistics')

    # ------------------------------------------------------------------------
    custom = parser.add_argument_group('customization')

    custom.add_argument('--resample-method',
                        action='store',
                        dest='resample_method',
                        choices=['near', 'bilinear', 'cubic',
                                 'cubicspline', 'lanczos'],
                        default='near',
                        help='Resampling method to use')

    custom.add_argument('--pixel-size',
                        action='store',
                        dest='pixel_size',
                        default=None,
                        metavar='FLOAT',
                        help='Pixel size for the output product')

    custom.add_argument('--pixel-size-units',
                        action='store',
                        dest='pixel_size_units',
                        choices=['meters', 'dd'],
                        default=None,
                        help='Units for the pixel size')

    custom.add_argument('--extent-units',
                        action='store',
                        dest='extent_units',
                        choices=['meters', 'dd'],
                        default='meters',
                        help='Units for the extent')

    custom.add_argument('--extent-minx',
                        action='store',
                        dest='extent_minx',
                        default=None,
                        metavar='FLOAT',
                        help='Minimum X direction extent value')

    custom.add_argument('--extent-maxx',
                        action='store',
                        dest='extent_maxx',
                        default=None,
                        metavar='FLOAT',
                        help='Maximum X direction extent value')

    custom.add_argument('--extent-miny',
                        action='store',
                        dest='extent_miny',
                        default=None,
                        metavar='FLOAT',
                        help='Minimum Y direction extent value')

    custom.add_argument('--extent-maxy',
                        action='store',
                        dest='extent_maxy',
                        default=None,
                        metavar='FLOAT',
                        help='Maximum Y direction extent value')

    custom.add_argument('--target-projection',
                        action='store',
                        dest='target_projection',
                        choices=['sinu', 'aea', 'utm', 'ps', 'lonlat'],
                        default=None,
                        help='Reproject to this projection')

    custom.add_argument('--false-easting',
                        action='store',
                        dest='false_easting',
                        default=None,
                        metavar='FLOAT',
                        help='False Easting reprojection value')

    custom.add_argument('--false-northing',
                        action='store',
                        dest='false_northing',
                        default=None,
                        metavar='FLOAT',
                        help='False Northing reprojection value')

    custom.add_argument('--datum',
                        action='store',
                        dest='datum',
                        choices=['wgs84', 'nad27', 'nad83'],
                        default=None,
                        help='Datum to use during reprojection')

    custom.add_argument('--utm-north-south',
                        action='store',
                        dest='utm_north_south',
                        choices=['north', 'south'],
                        default=None,
                        help='UTM North or South')

    custom.add_argument('--utm-zone',
                        action='store',
                        dest='utm_zone',
                        default=None,
                        metavar='INT',
                        help='UTM Zone reprojection value')

    custom.add_argument('--central-meridian',
                        action='store',
                        dest='central_meridian',
                        default=None,
                        metavar='FLOAT',
                        help='Central Meridian reprojection value')

    custom.add_argument('--latitude-true-scale',
                        action='store',
                        dest='latitude_true_scale',
                        default=None,
                        metavar='FLOAT',
                        help='Latitude True Scale reprojection value')

    custom.add_argument('--longitude-pole',
                        action='store',
                        dest='longitude_pole',
                        default=None,
                        metavar='FLOAT',
                        help='Longitude Pole reprojection value')

    custom.add_argument('--origin-latitude',
                        action='store',
                        dest='origin_latitude',
                        default=None,
                        metavar='FLOAT',
                        help='Origin Latitude reprojection value')

    custom.add_argument('--std-parallel-1',
                        action='store',
                        dest='std_parallel_1',
                        default=None,
                        metavar='FLOAT',
                        help='Standard Parallel 1 reprojection value')

    custom.add_argument('--std-parallel-2',
                        action='store',
                        dest='std_parallel_2',
                        default=None,
                        metavar='FLOAT',
                        help='Standard Parallel 2 reprojection value')

    # ------------------------------------------------------------------------
    developer = parser.add_argument_group('developer')

    developer.add_argument('--dev-mode',
                           action='store_true',
                           dest='dev_mode',
                           default=False,
                           help='Specify developer mode')

    developer.add_argument('--dev-intermediate',
                           action='store_true',
                           dest='dev_intermediate',
                           default=False,
                           help='Specify keeping intermediate data files')

    developer.add_argument('--debug',
                           action='store_true',
                           dest='debug',
                           default=False,
                           help='Specify debug logging')

    return parser


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
    cli_args = parse_command_line()
    configure_base_logger(level='debug' if cli_args.get('debug') else 'info')
    processor.get_instance(cfg.get('processing'), cli_args).process()
