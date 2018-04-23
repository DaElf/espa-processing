
import os
import shutil
import tempfile

import pytest

from processing import staging

def test_dirs_to_make():
    basedir = '/path/to/working/dir'
    subdirs = ['mynewdir']
    assert len(subdirs) == len(staging.dirs_to_make(basedir, subdirs))
    assert staging.dirs_to_make(basedir, subdirs)[0].endswith(subdirs[0] )

@pytest.fixture
def temporary_dir():
    fullpath = './make/path/here/'
    yield fullpath
    shutil.rmtree(fullpath, ignore_errors=True)

def test_init_dirs(temporary_dir):
    assert not os.path.exists(temporary_dir)
    staging.initialize_processing_directory(temporary_dir)
    assert os.path.exists(temporary_dir)
