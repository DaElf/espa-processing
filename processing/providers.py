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
                for x,y in yaml.safe_load(open(fp)).items()]
                )


def make_cmd(entity, extras=None):
    """ Convert YAML entry into commandline call

    Args:
        entity (dict): The serialzied represntation of command
        extras (dict): format values to insert into arg calls

    Returns:
        str: The formatted string

    Example:
        >>> make_cmd({"cmd": "echo", "args": "hello"})
        'echo hello'
    """
    args = ' '.join('{} {}'.format(x, y.format(**extras)) for z in entity.get('args', []) for x, y in z.items())
    return '{cmd} {args}'.format(args=args, cmd=entity['cmd']) if 'cmd' in entity else ''


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
    strip_reqs = lambda x: {k: v for k, v in x.items() if k != 'requires'}
    def pull_reqs(r):
        if isinstance(r, dict):
            return r.values()[0].get('requires')
        return r

    def recur_reqs(x, providers):
        if isinstance(x.get('requires'), list):
            return fetch_requires(x.get('requires'), providers) + [strip_reqs(x)]
        return [x]

    return [y for z in [recur_reqs(providers.get(x), providers)
            for x in pull_reqs(requires)] for y in z ]


def find_all(provider_path='processing/'):
    from functools import reduce
    from operator import add
    return reduce(add, [v.get('products')
                        for v in read_yaml(provider_path).values()
                            if 'products' in v])


import logging
def sequence(product, provider_path='processing/', **kwargs):
    # TODO: docstring
    logging.info('FIND A PROVIDER FOR: %s', product)
    a = read_yaml(provider_path)
    p = find_product(product, a)
    logging.info('FIND PRODUCT: %s', p)
    if p:
        r = fetch_requires(p, a)
        return '; '.join(filter(None, [make_cmd(e, kwargs) for e in r] + [make_cmd(p.values()[0], kwargs)]))
    else:
        raise IOError('Product %s not found in providers' % product)
