from git_sh_sync.proc import Command


def test_cmd_echo():
    content = 'test test'
    res = Command('echo "{}"'.format(content))
    assert res() is True
    assert res.cmd == ['echo', content]
    assert res.cwd is None
    assert res.cin is None
    assert res.exc is None
    assert res.code == 0
    assert res.out == [content]
    assert res.stdout == content
    assert res.err == []
    assert res.stderr == ''
    assert res.success is True
    assert res.launched is True


def test_cmd_ls_cwd(rootdir):
    files = ('makefile', 'readme.rst', 'requirements.txt')
    res = Command('ls -1', cwd=rootdir.root)
    assert res() is True
    assert res.cmd == ['ls', '-1']
    assert res.cwd == rootdir.root
    assert res.code == 0
    assert res.success is True
    assert res.stderr == ''
    assert res.err == []
    for name in files:
        assert name in res.stdout
        assert name in res.out


def test_cmd_cat_stdin():
    content = 'test test'
    res = Command('cat', cin=content)
    assert res() is True
    assert res.stderr == ''
    assert res.err == []
    assert res.stdout == content
    assert res.out == [content]


def test_cmd_no_double():
    res = Command('echo')
    assert res.success is False
    assert res.launched is False

    assert res() is True
    assert res.success is True
    assert res.launched is True

    assert res() is False
    assert res.success is True
    assert res.launched is True


def test_cmd_error():
    res = Command('this-is-not-a-command')
    assert res.code is None
    assert res.success is False
    assert res.launched is False

    assert res() is False
    assert res.code is None
    assert res.success is False
    assert res.launched is True

    assert isinstance(res.exc, OSError)
