""" Defines JSON validation de-/serialization """
import datetime

from marshmallow import Schema, fields, pre_load, validate, ValidationError


VALID_OUTPUT_FORMATS = ['envi', 'gtiff', 'hdf-eos2', 'netcdf']
VALID_RESAMPLE_METHODS = ['near', 'bilinear', 'cubic', 'cubicspline',
                          'lanczos']
VALID_PIXEL_SIZE_UNITS = ['meters', 'dd']
VALID_IMAGE_EXTENTS_UNITS = ['meters', 'dd']
VALID_PROJECTIONS = ['sinu', 'aea', 'utm', 'ps', 'lonlat']
VALID_NS = ['north', 'south']
VALID_DATUMS = ['WGS84', 'NAD27', 'NAD83']


class ClipSchema(Schema):
    image_extents_units = fields.String(validate=validate.ContainsOnly(VALID_IMAGE_EXTENTS_UNITS), missing='meters')
    maxx = fields.Float()
    maxy = fields.Float()
    minx = fields.Float()
    miny = fields.Float()


class CustomizationOptsSchema(Schema):
    output_format = fields.String(validate=validate.ContainsOnly(VALID_OUTPUT_FORMATS))
    pixel_size = fields.Float(missing=30.0)
    pixel_size_units = fields.String(validate=validate.ContainsOnly(VALID_PIXEL_SIZE_UNITS))
    resample_method = fields.String(validate=validate.ContainsOnly(VALID_RESAMPLE_METHODS))


class LatlonProjectionOptsSchema(Schema):
    datum = fields.String(required=False, missing='WGS84',
                          validate=validate.ContainsOnly(VALID_DATUMS))


class PsProjectionOptsSchema(Schema):
    latitude_true_scale = fields.Float(validate=(
        validate.Range(min=-90.0, max=-60.0),
        validate.Range(min=60.0, max=90.0)))
    longitude_pole = fields.Float()
    origin_lat = fields.Float(validate=validate.ContainsOnly([-90.0, 90.0]))
    false_easting = fields.Float()
    false_northing = fields.Float()
    datum = fields.String(required=False, missing='WGS84',
                          validate=validate.ContainsOnly(VALID_DATUMS))


class UtmProjectionOptsSchema(Schema):
    utm_zone = fields.Int(validate=validate.Range(min=0, max=60))
    utm_north_south = fields.String(validate=validate.ContainsOnly(VALID_NS))
    datum = fields.String(required=False, missing='WGS84',
                          validate=validate.ContainsOnly(VALID_DATUMS))


class SinuProjectionOptsSchema(Schema):
    central_meridian = fields.Float()
    false_easting = fields.Float()
    false_northing = fields.Float()
    datum = fields.String(required=False, missing='WGS84',
                          validate=validate.ContainsOnly(VALID_DATUMS))


class AeaProjectionOptsSchema(Schema):
    central_meridian = fields.Float()
    std_parallel_1 = fields.Float()
    std_parallel_2 = fields.Float()
    origin_lat = fields.Float()
    false_easting = fields.Float()
    false_northing = fields.Float()
    datum = fields.String()


class AvailableProductsSchema(Schema):
    """ Supported options for processing """
    include_cfmask = False
    include_customized_source_data = False
    include_dswe = False
    include_lst = False
    include_source_data = False
    include_source_metadata = False
    include_sr = False
    include_sr_evi = False
    include_sr_msavi = False
    include_sr_nbr = False
    include_sr_nbr2 = False
    include_sr_ndmi = False
    include_sr_ndvi = False
    include_sr_savi = False
    include_sr_thermal = False
    include_sr_toa = False
    include_statistics = False


class ProcessingRequestSchema(Schema):
    bridge_mode = False
    download_url = "DOWNLOAD_URL"
    espa_api = "skip_api"
    options = fields.Nested(AvailableProductsSchema)
    orderid = "ORDER_ID"
    product_type = "PRODUCT_TYPE"
    scene = "SCENE_ID"
