import pytest

from processing import providers


@pytest.fixture(params=[4,5,7,8])
def lsat_id(request ):
    return {
        4: 'LT04_L1TP_030031_19890420_20161002_01_T1',
        5: 'LT05_L1TP_032028_20120425_20160830_01_T1',
        7: 'LE07_L1TP_028028_20130510_20160908_01_T1',
        8: 'LC08_L1TP_015035_20140713_20170304_01_T1'
    }[request.param]


@pytest.fixture(params=['T', 'A'])
def modis_id(request ):
    return {
        "A": 'MYD09GA.A2017089.h12v02.005.2017091074612',
        "T": 'MOD13Q1.A2000353.h27v07.006.2015148800230',
    }[request.param]


def test_no_yaml_found():
    assert {} == providers.read_yaml('/path/does/not/exist')
    assert {} == providers.read_yaml('processing', '*.notafile')

@pytest.fixture(scope='module')
def provider_path():
    import os
    if os.path.isdir('processing'):
        return 'processing'
    else:
        raise IOError('WHAt!')

def test_ok_yaml_found(provider_path):
    assert {} != providers.read_yaml(provider_path)
    assert len(providers.read_yaml(provider_path).keys()) > 0

def test_make_cmd():
    cmd = 'echo hello'
    assert cmd == providers.make_cmd({"cmd": "echo", "args": "hello"})


def test_find_product():
    mock_providers = {'i1': {'products': ['thing']}}
    assert mock_providers == providers.find_product('thing', mock_providers)


def test_fetch_requires():
    p = {'cook': {'requires': ['grocery']}}
    ps = {'grocery': {'cmd': 'go_to_market'}}
    expected = [{'cmd': 'go_to_market'}]
    assert expected == providers.fetch_requires(p, ps)

def test_fetch_requires_nested():
    p = {'cook': {'requires': ['grocery']}}
    ps = {'grocery': {'cmd': 'go_to_market', 'requires': ['car']},
          'car': {'cmd': 'buy_car'}}
    expected = [{'cmd': 'buy_car'}, {'cmd': 'go_to_market'}]
    assert expected == providers.fetch_requires(p, ps)

def test_lpgs_to_espa(lsat_id, provider_path):
    product = 'espa_landsat'
    cmd = 'convert_lpgs_to_espa --mtl {}_MTL.txt'.format(lsat_id)
    assert providers.sequence(product, product_id=lsat_id) == cmd

def test_toa_command(lsat_id, provider_path):
    product = 'toa_refl'
    cmd = 'surface_reflectance.py --xml {}.xml --write-sr False'.format(lsat_id)
    assert providers.sequence(product, product_id=lsat_id) == cmd

def test_bt_command(lsat_id):
    product = 'toa_bt'
    cmd = 'surface_reflectance.py --xml {}.xml --write-sr False'.format(lsat_id)
    assert providers.sequence(product, product_id=lsat_id) == cmd

def test_sr_command_l8(lsat_id):
    product = 'sr_refl'
    cmd = 'surface_reflectance.py --xml {}.xml --write-sr False'.format(lsat_id)
    assert providers.sequence(product, product_id=lsat_id) == cmd

def test_sr_command_l7(lsat_id):
    product = 'sr_refl'
    cmd = 'surface_reflectance.py --xml {}.xml --write-sr False'.format(lsat_id)
    assert providers.sequence(product, product_id=lsat_id) == cmd

def test_st_command(lsat_id):
    product = 'st'
    cmd = 'surface_reflectance.py --xml {}.xml --write-sr False'.format(lsat_id)
    assert providers.sequence(product, product_id=lsat_id) == cmd

def test_sw_command(lsat_id):
    product = 'sw'
    cmd = 'surface_reflectance.py --xml {}.xml --write-sr False'.format(lsat_id)
    assert providers.sequence(product, product_id=lsat_id) == cmd

def test_modis_command(modis_id):
    product = 'espa_modis'
    cmd = 'convert_modis_to_espa --hdf {}.hdf'.format(modis_id)
    assert providers.sequence(product, product_id=modis_id) == cmd

def test_reproject_command(modis_id):
    product = 'gtif'
    cmd = 'convert_espa_to_gtif --xml {0}.xml --gtif {0}.tif'.format(modis_id)
    assert providers.sequence(product, product_id=modis_id) == cmd
