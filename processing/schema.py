""" Defines JSON validation de-/serialization """
import datetime

from marshmallow import Schema, fields, pre_load, validate, ValidationError

import sensor


VALID_PRODUCT_TYPES = ['landsat', 'modis']
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
    customization = fields.Nested(CustomizationOptsSchema)
    extents = fields.Nested(ClipSchema)
    projection = fields.Nested((
        AeaProjectionOptsSchema,
        SinuProjectionOptsSchema,
        UtmProjectionOptsSchema,
        PsProjectionOptsSchema,
        LatlonProjectionOptsSchema,
    ))


class SupportedSensorsField(fields.String):
    """ Ensures support for the produt id supplied """
    def _deserialize(self, value, attr, data):
        _ = sensor.info(value)
        return super(SupportedSensorsField, self)._deserialize(value, attr, data)

class MetadataSchema(Schema):
    orderid = fields.String(required=True)

class ProcessingRequestSchema(Schema):
    options = fields.Nested(AvailableProductsSchema, required=True)
    metadata = fields.Nested(MetadataSchema, required=True)
    input_name = SupportedSensorsField(required=True)
    input_urls = fields.List(fields.String(validate=validate.URL()), required=True)
