
import os
import shutil

import pytest

from processing import initialization

def test_dirs_to_make():
    basedir = '/path/to/working/dir'
    subdirs = ['mynewdir']
    assert len(subdirs) == len(initialization.dirs_to_make(basedir, subdirs))
    assert initialization.dirs_to_make(basedir, subdirs)[0].endswith(subdirs[0] )

@pytest.fixture
def temporary_dir():
    fullpath = '/path/to/working/dir'
    yield fullpath
    shutil.rmtree(fullpath, ignore_errors=True)

def test_init_dirs(temporary_dir):
    assert not os.path.exists(temporary_dir)
    initialization.initialize_processing_directory(temporary_dir)
    assert os.path.exists(temporary_dir)
