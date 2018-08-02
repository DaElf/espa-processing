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

    output = ''
    try:
        output = check_output(['gpg', '--yes', '--sign', '--armor', sum_file])
    except IOError as e:
        logger.warn("I/O error on '%s': %s" % (e.filename, e.strerror))
    except CalledProcessError as e:
        logger.warn("gpg failed: %s" % (str(e)))
    except OSError as e:
        logger.warn("failed to run 'gpg': %s" % (str(e)))
    finally:
        if len(output) > 0:
            self._logger.info(output)
