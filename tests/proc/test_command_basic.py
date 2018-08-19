from os import path
from pprint import pformat

from git_sh_sync.proc import CHAR_NEWLINE


def test_cmd_init_empty(helpcmd):
    res = helpcmd.init('test-command')
    assert res.cmd == ['test-command']
    assert res.cwd is None
    assert res.cin is None
    assert res.exc is None
    assert res.code is None
    assert res.stdout == ''
    assert res.stderr == ''
    assert res.command == 'test-command'
    assert res.launched is False
    assert res.success is False
    assert res.out == []
    assert res.err == []


def test_cmd_init_more(helpcmd):
    res = helpcmd.init('test-command', cwd='test-dir', cin='test-input')
    assert res.cmd == ['test-command']
    assert res.cwd == path.realpath('test-dir')
    assert res.cin == 'test-input'
    assert res.exc is None
    assert res.code is None
    assert res.stdout == ''
    assert res.stderr == ''
    assert res.command == 'test-command'
    assert res.launched is False
    assert res.success is False
    assert res.out == []
    assert res.err == []


def test_cmd_out_err(helpcmd):
    res = helpcmd.init('test-command')
    assert res.cmd == ['test-command']
    assert res.stdout == ''
    assert res.out == []
    assert res.stderr == ''
    assert res.err == []
    helpcmd.edit(res, stdout='test\nout', stderr='test\nerr')
    assert res.stdout == 'test\nout'
    assert res.out == ['test', 'out']
    assert res.stderr == 'test\nerr'
    assert res.err == ['test', 'err']


def test_cmd_launched_c(helpcmd):
    res = helpcmd.init('test-command')
    assert res.cmd == ['test-command']
    assert res.code is None
    assert res.launched is False
    helpcmd.edit(res, code=0)
    assert res.code == 0
    assert res.launched is True


def test_cmd_launched_e(helpcmd):
    res = helpcmd.init('test-command')
    assert res.cmd == ['test-command']
    assert res.exc is None
    assert res.launched is False
    helpcmd.edit(res, exc='exception')
    assert res.exc == 'exception'
    assert res.launched is True


def test_cmd_fields_pre(helpcmd):
    res = helpcmd.init('test-command', cwd='test-dir', cin='test-input')
    assert res.fields == dict(
        command='test-command',
        cwd=path.realpath('test-dir'),
        cin='test-input',
    )


def test_cmd_repr_pre(helpcmd):
    res = helpcmd.init('test-command', cwd='test-dir', cin='test-input')
    assert str(res) == pformat(dict(
        command='test-command',
        cwd=path.realpath('test-dir'),
        cin='test-input',
    ))


def test_cmd_fields_post(helpcmd):
    res = helpcmd.init('test-command', cwd='test-dir', cin='test-input')
    assert res.fields == dict(
        command='test-command',
        cwd=path.realpath('test-dir'),
        cin='test-input',
    )
    helpcmd.edit(res, code=0)
    assert res.fields == dict(
        command='test-command',
        cwd=path.realpath('test-dir'),
        cin='test-input',
        stdout='',
        stderr='',
        code=0,
        exc=None,
    )


def test_cmd_repr_post(helpcmd):
    res = helpcmd.init('test-command', cwd='test-dir', cin='test-input')
    assert str(res) == pformat(dict(
        command='test-command',
        cwd=path.realpath('test-dir'),
        cin='test-input',
    ))
    helpcmd.edit(res, code=0)
    assert str(res) == pformat(dict(
        command='test-command',
        cwd=path.realpath('test-dir'),
        cin='test-input',
        stdout='',
        stderr='',
        code=0,
        exc=None,
    ))


def test_cmd_repr_repr(helpcmd):
    res = helpcmd.init('test-command', cwd='test-dir', cin='test-input')
    assert res.repr == '"""{}{}{}"""'.format(
        CHAR_NEWLINE, str(res), CHAR_NEWLINE
    )
