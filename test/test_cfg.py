import os
import mock

import pytest

from processing import cfg


@mock.patch.dict('os.environ', {'ESPA_PROC_CONFIG_KEY': 'george'})
def test_environ():
    assert cfg.get('config')['KEY'] == 'george'
    assert 'key' in cfg.get('config', lower=True)

def test_config_not_found():
    with mock.patch.dict('os.environ'):
        os.environ.clear()
        os.environ['ESPA_PROC_CONFIG_PATH'] = '/path/to/nowhere'
        assert {} == cfg.get('db')
        assert 'path' in cfg.get('config', lower=True)

@mock.patch.dict('os.environ', {'ESPA_PROC_CONFIG_PATH': './run/config.ini'})
def test_local_config():
    assert 'key' in cfg.get('config', lower=True)
