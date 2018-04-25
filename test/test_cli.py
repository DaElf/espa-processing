#!/usr/bin/env python

import argparse

import pytest

from processing import cli


def test_reconstruct_group_schema():
    parser = argparse.ArgumentParser()
    group1 = parser.add_argument_group('group1')
    group1.add_argument('--test1')
    args = parser.parse_args('--test1 one'.split())
    expected = {'group1': {'test1': 'one'}}
    assert expected == cli.reconstruct_group_schema(parser, args)


def test_clear_all_none():
    expected = {'a': 1}
    assert expected == cli.clear_all_none({'a': 1, 'b': {'c': None}})


def test_stack_projection_args():
    expected = {'utm': {'zone': 10}}
    assert expected == cli.stack_projection_args({'target_projection': 'utm', 'zone': 10})


@pytest.fixture(scope="module")
def parser():
    return cli.build_command_line_parser()


@pytest.fixture(scope='function')
def options():
    return ['--order-id', 'ORDERID',
            '--input-product-id', 'LT04_L1TP_030031_19890420_20161002_01_T1',
            '--input-url', 'file://',
            '--product-type', 'landsat']


def test_missing_options(parser, options):
    options.pop(0)
    with pytest.raises(SystemExit):
        args = parser.parse_args(options)


def test_invalid_options(parser, options):
    options.extend(['--this-is-not-real', 'bad-bad'])
    with pytest.raises(SystemExit):
        args = parser.parse_args(options)
