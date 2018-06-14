from subprocess import check_output, CalledProcessError, check_call
import glob
import sys
import os
import tempfile
import logging
import settings
from logging_tools import EspaLogging


def distribute_sum_directory(path='.', product_name='sum'):

    logger = EspaLogging.get_logger(settings.PROCESSING_LOGGER)

    sum_list = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            sum_list.append(os.path.join(path, name))

    sum_file = product_name + '.sha256'
    try:
    # sha 256 sum all the files
        print("Including sha56 sum off all files")
        cmd = ["sha256sum"] + sum_list
        logger.info("Running: sha256sum")
        fout=open(sum_file, 'w')
        check_call(cmd, stdout=fout)
    except IOError as e:
        logger.error("I/O error on '%s': %s" % (e.filename, e.strerror))
        raise
    except CalledProcessError as e:
        logger.error("sha256sum failed: %s" % (str(e)))
        raise
    except OSError as e:
        logger.error("failed to run 'sha256sum': %s" % (str(e)))
        raise

    try:
        #tempdir = tempfile.mkdtemp()
        #check_output(['gpg','--homedir',tempdir,'--import','USGS_private.asc'])
        #check_output(['gpg','--homedir',tempdir,'--detach-sig','--armor','sum.sha256'])
        check_output(['gpg', '--yes', '--sign', '--armor', sum_file])
    except IOError as e:
        logger.error("I/O error on '%s': %s" % (e.filename, e.strerror))
    except CalledProcessError as e:
        logger.error("gpg failed: %s" % (str(e)))
    except OSError as e:
        logger.error("failed to run 'gpg': %s" % (str(e)))
