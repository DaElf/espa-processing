""" Defines JSON validation de-/serialization """
import datetime

from marshmallow import Schema, fields, pre_load, validate, validates, ValidationError

import sensor


VALID_PRODUCT_TYPES = ['landsat', 'modis']
VALID_OUTPUT_FORMATS = ['envi', 'gtiff', 'hdf-eos2', 'netcdf']
VALID_RESAMPLE_METHODS = ['near', 'bilinear', 'cubic', 'cubicspline',
                          'lanczos']
VALID_PIXEL_SIZE_UNITS = ['meters', 'dd']
VALID_IMAGE_EXTENTS_UNITS = ['meters', 'dd']
VALID_PROJECTIONS = ['sinu', 'aea', 'utm', 'ps', 'lonlat']
VALID_NS = ['north', 'south']
VALID_DATUMS = ['wgs84', 'nad27', 'nad83']


class ClipSchema(Schema):
    image_extents_units = fields.String(validate=validate.OneOf(VALID_IMAGE_EXTENTS_UNITS), missing='meters')
    maxx = fields.Float(required=True)
    maxy = fields.Float(required=True)
    minx = fields.Float(required=True)
    miny = fields.Float(required=True)


class CustomizationOptsSchema(Schema):
    output_format = fields.String(required=True,
                                  validate=validate.OneOf(VALID_OUTPUT_FORMATS))
    pixel_size = fields.Float(required=False, missing=30.0)
    pixel_size_units = fields.String(required=False, missing='meters',
                                     validate=validate.OneOf(VALID_PIXEL_SIZE_UNITS))
    resample_method = fields.String(required=False, missing='near',
                                    validate=validate.OneOf(VALID_RESAMPLE_METHODS))


class LatlonProjectionOptsSchema(Schema):
    datum = fields.String(required=False, missing='wgs84',
                          validate=validate.OneOf(VALID_DATUMS))


class PsProjectionOptsSchema(Schema):
    latitude_true_scale = fields.Float(required=True)
    longitude_pole = fields.Float(required=True)
    origin_latitude = fields.Float(required=True,
                                   validate=validate.OneOf([-90.0, 90.0]))
    false_easting = fields.Float(required=False, missing=0.0)
    false_northing = fields.Float(required=False, missing=0.0)
    datum = fields.String(required=False, missing='wgs84',
                          validate=validate.OneOf(VALID_DATUMS))

    @validates('latitude_true_scale')
    def check_polar(self, value):
        if not 60.0 <= abs(value) <= 90.0:
            raise ValidationError('Must be between (-60.0 and -90.0) or (60.0 and 90.0)')


class UtmProjectionOptsSchema(Schema):
    utm_zone = fields.Int(required=True,
                          validate=validate.Range(min=0, max=60))
    utm_north_south = fields.String(required=True,
                                    validate=validate.OneOf(VALID_NS))
    datum = fields.String(required=False, missing='wgs84',
                          validate=validate.OneOf(VALID_DATUMS))


class SinuProjectionOptsSchema(Schema):
    central_meridian = fields.Float(required=True)
    false_easting = fields.Float(required=False, missing=0.0)
    false_northing = fields.Float(required=False, missing=0.0)
    datum = fields.String(required=False, missing='wgs84',
                          validate=validate.OneOf(VALID_DATUMS))


class AeaProjectionOptsSchema(Schema):
    central_meridian = fields.Float(required=True)
    std_parallel_1 = fields.Float(required=True)
    std_parallel_2 = fields.Float(required=True)
    origin_latitude = fields.Float(required=True)
    false_easting = fields.Float(required=False, missing=0.0)
    false_northing = fields.Float(required=False, missing=0.0)
    datum = fields.String(required=False, missing='wgs84',
                          validate=validate.OneOf(VALID_DATUMS))


class ProjectionSchema(Schema):
    aea = fields.Nested(AeaProjectionOptsSchema)
    sinu = fields.Nested(SinuProjectionOptsSchema)
    utm = fields.Nested(UtmProjectionOptsSchema)
    ps = fields.Nested(PsProjectionOptsSchema)
    latlon = fields.Nested(LatlonProjectionOptsSchema)


class SupportedSensorsField(fields.String):
    """ Ensures support for the produt id supplied """
    def _deserialize(self, value, attr, data):
        try:
            _ = sensor.info(value)
            return super(SupportedSensorsField, self)._deserialize(value, attr, data)
        except sensor.ProductNotImplemented:
            raise ValidationError('Product not implemented')


class MetadataSchema(Schema):
    order_id = fields.String(required=True)


class ProcessingRequestSchema(Schema):
    metadata = fields.Nested(MetadataSchema, required=True)
    input_name = SupportedSensorsField(required=True)
    input_urls = fields.List(fields.String(required=True,
                             validate=validate.Regexp('(http|https|file)[:][/]{2}.*')))
    customization = fields.Nested(CustomizationOptsSchema, required=False)
    extents = fields.Nested(ClipSchema, required=False)
    projection = fields.Nested(ProjectionSchema, required=False)


def load(parms):
    return ProcessingRequestSchema().load(parms)
