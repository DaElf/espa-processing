
'''
Description: Provides the implementation for creating the core directories
             required for the processing of a product request.

'''

import os
import shutil
import logging


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
    """
    if os.path.exists(base_work_dir):
        logging.warning('Removing processing directory: %s', base_work_dir)
        shutil.rmtree(base_work_dir, ignore_errors=True)

    logging.info('Create processing directory: %s', base_work_dir)
    os.makedirs(base_work_dir, mode=0755)

    for folder in dirs_to_make(base_work_dir, directories):
        logging.debug('Create directory: %s', folder)
        os.makedirs(folder, mode=0755)
