""" Abstraction for interfacing with providers.yml """

import yaml


def read_yaml(filename='processing/providers.yaml'):
    """ Parse a YAML file from filesystem

    Args:
        filename (str): relative path to providers yaml

    Returns:
        dict: serialized data from file
    """
    return yaml.load(open(filename))


def make_cmd(entity):
    """ Convert YAML entry into commandline call

    Args:
        entity (dict): The serialzied represntation of command

    Returns:
        str: The formatted string

    Example:
        >>> make_cmd({"cmd": "echo", "args": "hello"})
        'echo hello'
    """
    return '{cmd} {args}'.format(**entity)


def find_product(product, providers):
    func = lambda x: product in x['products']
    return filter(func, providers)


def sequence(product, input_id):
    a = read_yaml()
    p = find_product(product, a)
