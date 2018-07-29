from os import environ, path

from git_sh_sync.util.disk import joined


def test_joined_empty():
    res = joined('')
    assert res == path.realpath('.')


def test_joined_realpath():
    res = joined('test')
    assert res == path.realpath('test')


def test_joined_expandvars():
    res = joined('$HOME')
    assert res == environ.get('HOME')


def test_joined_expanduser():
    res = joined('~')
    assert res == environ.get('HOME')


def test_joined_join():
    res = joined('test', 'test', 'test')
    assert res == path.realpath(path.join('test', 'test', 'test'))


def test_joined_leading():
    res = joined('/test', '/test', '/test')
    assert res == path.realpath(path.join(path.sep, 'test', 'test', 'test'))


def test_joined_relative():
    res = joined('/test', 'test', 'test', '..')
    assert res == path.realpath(path.join(path.sep, 'test', 'test'))
