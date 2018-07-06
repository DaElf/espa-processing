

import os
from ConfigParser import ConfigParser


def get_cfg_file_path(filename):
    """Build the full path to the config file

    Args:
        filename (str): The name of the file to append to the full path.

    Raises:
        Exception(message)
    """

    if 'ESPA_CONFIG_PATH' in os.environ:
        config_path = os.path.join(os.environ.get('ESPA_CONFIG_PATH'), filename)
        if os.path.isfile(config_path):
            return config_path

    # Use the users home directory as the base source directory for
    # configuration
    if 'HOME' in os.environ:
        config_path = os.path.join(os.environ.get('HOME'), '.usgs', 'espa', filename)
        if os.path.isfile(config_path):
            return config_path

    config_path = os.path.join(os.path.join(os.getcwd(), filename))
    if os.path.isfile(config_path):
        return config_path

    return None


def retrieve_cfg(cfg_filename):
    """Retrieve the configuration for the cron

    Returns:
        cfg (ConfigParser): Configuration for ESPA cron.

    Raises:
        Exception(message)
    """

    # Build the full path to the configuration file
    config_path = get_cfg_file_path(cfg_filename)

    if not config_path:
        raise Exception('Missing configuration file [{}]'.format(config_path))

    # Create the object and load the configuration
    cfg = ConfigParser()
    cfg.read(config_path)

    return cfg

