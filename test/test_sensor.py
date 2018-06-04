#!/usr/bin/env python

import pytest

# from processing import sensor
# 
# 
# class TestSensor(object):
#     """Test a few things, and expand on it someday"""
#     terra_product_id = 'MOD09GQ.A2000072.h02v09.005.2008237032813'
#     aqua_product_id = 'MYD09GQ.A2000072.h02v09.005.2008237032813'
#     lt04_product_id = 'LT04_L1TP_038038_19950624_20160302_01_T1'
#     lt05_product_id = 'LT05_L1TP_038038_19950624_20160302_01_T1'
#     le07_product_id = 'LE07_L1TP_038038_19950624_20160302_01_T1'
#     lc08_product_id = 'LC08_L1TP_038038_19950624_20160302_01_T1'
#     lt08_product_id = 'LT08_L1TP_038038_19950624_20160302_01_T1'
#     lo08_product_id = 'LO08_L1TP_038038_19950624_20160302_01_T1'
#     non_product_id = 'chuck'
# 
#     def test_is_sensor(self):
#         assert sensor.is_terra(self.terra_product_id)
#         assert sensor.is_aqua(self.aqua_product_id)
#         assert all(sensor.is_modis(x) for x in (
#             self.aqua_product_id, self.terra_product_id))
#         assert sensor.is_landsat4(self.lt04_product_id)
#         assert sensor.is_landsat5(self.lt05_product_id)
#         assert sensor.is_landsat7(self.le07_product_id)
#         assert all(sensor.is_landsat8(x) for x in (
#             self.lc08_product_id, self.lt08_product_id, self.lo08_product_id))
#         assert all(sensor.is_landsat(x) for x in (
#             self.lt04_product_id, self.lt05_product_id, self.le07_product_id,
#             self.lc08_product_id, self.lt08_product_id, self.lo08_product_id))
# 
#     def test_modis_sensor_info(self):
#         result_1 = sensor.modis_sensor_info(self.terra_product_id)
#         result_2 = sensor.info(self.terra_product_id)
#         assert result_1 == result_2
# 
#         result_1 = sensor.modis_sensor_info(self.aqua_product_id)
#         result_2 = sensor.info(self.aqua_product_id)
#         assert result_1 == result_2
# 
#     def test_landsat_collection_sensor_info(self):
#         result_1 = sensor.landsat_sensor_info(self.lt04_product_id)
#         result_2 = sensor.info(self.lt04_product_id)
#         assert result_1 == result_2
# 
#         result_1 = sensor.landsat_sensor_info(self.lt05_product_id)
#         result_2 = sensor.info(self.lt05_product_id)
#         assert result_1 == result_2
# 
#         result_1 = sensor.landsat_sensor_info(self.le07_product_id)
#         result_2 = sensor.info(self.le07_product_id)
#         assert result_1 == result_2
# 
#         result_1 = sensor.landsat_sensor_info(self.lc08_product_id)
#         result_2 = sensor.info(self.lc08_product_id)
#         assert result_1 == result_2
# 
#         result_1 = sensor.landsat_sensor_info(self.lo08_product_id)
#         result_2 = sensor.info(self.lo08_product_id)
#         assert result_1 == result_2
# 
#     def test_non_product_sensor_info(self):
#         with pytest.raises(sensor.ProductNotImplemented, match=r'.*is not a supported product.*'):
#             sensor.info(self.non_product_id)
