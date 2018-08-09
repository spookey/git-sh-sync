from collections import namedtuple
from os import path

from pytest import fixture


@fixture(scope='session')
def rootdir():
    root = path.abspath(path.dirname(path.dirname(__file__)))

    yield namedtuple(
        'RootDir', ('root', 'join')
    )(
        root=root,
        join=lambda *locs: path.abspath(path.join(root, *locs))
    )
