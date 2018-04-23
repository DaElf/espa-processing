""" Graph for command sequence of a product from providers yaml """

import os
from glob import glob

import yaml


def read_yaml(filepath='processing', match='*.yaml'):
    """ Parse all YAML files from directory on filesystem

    Args:
        filepath (str): relative path to providers yaml store

    Returns:
        dict: serialized data from file
    """
    return dict([(x,y)
                for fp in glob(os.path.join(filepath, match))
                for x,y in yaml.load(open(fp)).items()]
                )


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
    """ Extracts only the provider which produces a product

    Args:
        product (str): producer to search providers for
        providers (dict): parsed yaml providers descriptions

    Returns:
        dict: single key entry from providers

    Example:
        >>> find_product('thing', {'i1': {'products': ['thing']}})
        {'i1': {'products': ['thing']}}
    """
    return {name: description for name, description in providers.items()
            if product in description.get('products', [])}


def fetch_requires(requires, providers):
    """ Finds the sub-providers required by current provider as adjacency list

    Args:
        requires (list): list of requirements to extract
        providers (dict): serialized provider descriptions

    Returns:
        list: ordered requirement entities

    Example:
        >>> p = {'cook': {'requires': ['grocery']}}
        >>> ps = {'grocery': {'cmd': 'go_to_market'}}
        >>> fetch_requires(p, ps)
        [{'cmd': 'go_to_market'}]
    """
    if isinstance(requires, dict):
        requires = requires.values()[0].get('requires')
    return [y for z in [
        fetch_requires(providers.get(x).get('requires'), providers)
        + [{k:v for k, v in providers.get(x).items() if k != 'requires'}]
            if isinstance(providers.get(x).get('requires'), list)
                else [providers.get(x)]
            for x in requires] for y in z ]


def sequence(product, input_id):
    a = read_yaml()
    p = find_product(product, a)
