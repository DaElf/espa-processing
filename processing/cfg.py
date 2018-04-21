""" Environment variables override default configurations from file """

import os
import ConfigParser


def from_env(section, prefix='ESPA_PROC'):
    """ Read configuration values from environment variables

    Args:
        section (str): the section of config to read
        prefix (str): prefix to section to search for

    Returns:
        dict: current config
    """
    prefix += '_{}_'.format(section.upper())
    return {k.split(prefix)[1]:v
            for k, v in os.environ.items() if k.startswith(prefix)}


def cfgfile(config_file=None):
    """ Path to configuration file; if not provided, read from env or default

    Args:
        config_file (str): path to config to override environment variable

    Returns:
        str: path to configuration
    """
    return config_file or os.getenv('ESPA_PROC_CONFIG_PATH',
                                    os.path.join(os.path.expanduser('~/.usgs'),
                                                 '.espa-processing.ini'))


def from_file(section, config_file=None):
    """ Read all configuration values from a section

    Args:
        section (str): the section to read
        config_file (str): path to a configuration file

    Returns:
        dict: current configuration
    """
    if not os.path.exists(cfgfile(config_file)):
        return {}
    config = ConfigParser.ConfigParser()
    config.read(cfgfile(config_file))
    return {opt.upper(): config.get(section, opt)
            for opt in config.options(section)}


def get(section, config_file=None, lower=False):
    """ Read config, first from file, override by env vars

    Args:
        section (str): section of config to read
        config_file (str): path to config file
        lower (bool): convert all keys to lowercase

    Returns:
        dict: current config
    """
    return {k.lower() if lower else k: v for k, v in
            dict(from_file(section, config_file), **from_env(section)).items()}
