from logging import DEBUG, ERROR, INFO

from git_sh_sync.proc import Command


def test_cmd_log_init(caplog):
    caplog.set_level(DEBUG)
    Command('echo')
    assert len(caplog.records) == 1

    rec = caplog.records[-1]
    assert rec.levelno == DEBUG
    assert 'command initialized: """%s"""' in rec.msg
    assert 'echo' in rec.args[-1]


def test_cmd_log_success(caplog):
    caplog.set_level(INFO)
    res = Command('echo')
    assert not caplog.records
    res()
    assert len(caplog.records) == 1

    rec = caplog.records[-1]
    assert rec.levelno == INFO
    assert 'command success: """%s"""' in rec.msg
    assert 'echo' in rec.args[-1]


def test_cmd_log_failed(caplog):
    caplog.set_level(ERROR)
    res = Command('this-is-not-a-command')
    assert not caplog.records
    res()
    assert len(caplog.records) == 1

    rec = caplog.records[-1]
    assert rec.levelno == ERROR
    assert 'command failed: """%s"""' in rec.msg
    assert 'this-is-not-a-command' in rec.args[-1]
