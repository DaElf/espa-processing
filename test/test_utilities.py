

import pytest

from processing import utilities


def test_untar_command():
    cmd = 'tar --directory /path/to/place -xvf my.tar.gz'
    assert cmd == utilities.untar_cmd('my.tar.gz', '/path/to/place')


def test_watch_stdout():
    results = utilities.watch_stdout(["echo", "Hello World!"])
    assert results == {'output': 'Hello World!', 'status': 0}

def test_watch_stdout_fail():
    results = utilities.watch_stdout(["false"])
    assert results == {'output': '', 'status': 1}

def test_execute_cmd():
    cmd = ["echo", "Hello World!"]
    assert utilities.watch_stdout(cmd) == utilities.execute_cmd(cmd)
    assert {'status': 0, 'output': 'Hello World!'} == utilities.execute_cmd(cmd)

def test_execute_cmd_raises():
    cmd = ["false"]
    assert {'status': 1, 'output': ''} == utilities.execute_cmd(cmd)
