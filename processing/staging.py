''' Provides routines for creating order directories and staging data '''

import os
import sys
import glob
import shutil
import logging

import cfg
import settings
import utilities
import transfer


def dirs_to_make(base_work_dir, directories=['output', 'stage', 'work']):
    """ Convert a base path and subfolders to list of absolute paths to make

    Args:
        base_work_dir (str): relative or absolute path to base working directory
        directories (list): all subfolders to create undir base dir

    Returns:
        list: the fully joined paths to all subdirs
    """
    base_work_dir = os.path.abspath(base_work_dir)
    return [os.path.join(base_work_dir, f) for f in directories]


def initialize_processing_directory(base_work_dir, directories=['output', 'stage', 'work']):
    """ Initializes the processing directory and subfolders

    Args:
        base_work_dir (str): relative or absolute path to base working directory
        directories (list): all subfolders to create undir base dir

    Returns:
        dict: created directories, keys by basename
    """
    new_directories = dict()
    if os.path.exists(base_work_dir):
        logging.warning('Removing processing directory: %s', base_work_dir)
        shutil.rmtree(base_work_dir, ignore_errors=True)

    logging.info('Create processing directory: %s', base_work_dir)
    utilities.create_directory(base_work_dir)

    for folder in dirs_to_make(base_work_dir, directories):
        logging.debug('Create directory: %s', folder)
        utilities.create_directory(folder)
        new_directories.update({os.path.basename(folder): folder})
    return new_directories


def copy_data_to_destination(filename, dest, unpack=None, remove_staged=True):
    """ Copy staged data from source to destination, optional unpackaging

    Args:
        filename (str): path location of files to transfer
        dest (str): path to folder for final files
        unpack (tuple): list of file extensions to unpack
        remove_staged (bool): flag to remove staged files when in destination

    Returns:
        None
    """
    if unpack and any(filename.endswith(x) for x in unpack):
        logging.debug('Unpack file %s to %s', filename, dest)
        utilities.untar_data(filename, dest)
        if remove_staged:
            logging.debug('Remove staged file %s', filename)
            os.unlink(filename)
    else:
        logging.debug('Copy file %s to %s', filename, dest)
        transfer.local_transfer_file(filename, dest, remove_original=remove_staged)


def stage_input_data(download_urls, staging='stage',
                     destination='working', unpack=None, remove_staged=True):
    """Stages the input data required for the processor

    Args:
        download_urls (list): accessible file locations
        staging (str): path to staging directory
        destination (str): path to existing output directory
        unpack (bool, tuple): flag to detect known archive/compressed formats
        remove_staged (bool): flag to remove staged files when in destination

    Returns:
        list: all new files in destination
    """
    logging.debug("DOWNLOAD URLS: %s", download_urls)
    for uri in download_urls:
        staged_files = transfer.download_file_url(uri, staging)
        copy_data_to_destination(staged_files, destination, unpack, remove_staged)
    return glob.glob(os.path.join(destination, '*'))
