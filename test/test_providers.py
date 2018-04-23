import pytest

from processing import providers


LT04_TEST_ID = 'LT04_L1TP_030031_19890420_20161002_01_T1'
LT05_TEST_ID = 'LT05_L1TP_032028_20120425_20160830_01_T1'
LE07_TEST_ID = 'LE07_L1TP_028028_20130510_20160908_01_T1'
LC08_TEST_ID = 'LC08_L1TP_015035_20140713_20170304_01_T1'


def test_make_cmd():
    cmd = 'echo hello'
    assert cmd == providers.make_cmd({"cmd": "echo", "args": "hello"})


def test_find_product():
    mock_providers = {'i1': {'products': ['thing']}}
    assert mock_providers == providers.find_product('thing', mock_providers)


def test_lpgs_to_espa(pid=LT04_TEST_ID):
    product = 'espa_landsat'
    cmd = 'lpgs_to_espa --mtl {}.mtl;'.format(pid)
    assert providers.sequence(product, pid) == cmd

def test_toa_command(pid=LT04_TEST_ID):
    product = 'toa_refl'
    cmd = ['surface_reflectance.py --xml {}.xml --write-sr False'.format(pid)]
    assert providers.sequence(product, pid) == cmd

def test_bt_command():
    assert 1 < 0

def test_sr_command_l8():
    assert 1 < 0

def test_sr_command_l7():
    assert 1 < 0

def test_st_command():
    assert 1 < 0

def test_sw_command():
    assert 1 < 0

def test_modis_command():
    assert 1 < 0

def test_reproject_command():
    assert 1 < 0
