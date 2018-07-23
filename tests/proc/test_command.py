from git_sh_sync.proc import command


def test_cmd_echo():
    content = 'test test'

    res = command('echo "{}"'.format(content))
    assert res.cmd == ['echo', content]
    assert res.cwd is None
    assert res.cin is None
    assert res.exc is None
    assert res.code == 0
    assert res.out == [content]
    assert res.stdout == content
    assert res.err == []
    assert res.stderr == ''


def test_cmd_ls_cwd(helpdir):
    res = command('ls -1', cwd=helpdir.root)
    assert res.cmd == ['ls', '-1']
    assert res.cwd == helpdir.root
    assert res.cin is None
    assert res.exc is None
    assert res.code == 0
    assert res.err == []
    assert res.stderr == ''
    for elem in ('makefile', 'readme.rst', 'requirements.txt'):
        assert elem in res.out
        assert elem in res.stdout


def test_cmd_cat_cin():
    content = 'test test'

    res = command('cat', cin=content)
    assert res.cmd == ['cat']
    assert res.cwd is None
    assert res.cin == content
    assert res.exc is None
    assert res.code == 0
    assert res.out == [content]
    assert res.stdout == content
    assert res.err == []
    assert res.stderr == ''


def test_cmd_error():
    res = command('this-is-not-a-command')
    assert res.cmd == ['this-is-not-a-command']
    assert res.cwd is None
    assert res.cin is None
    assert isinstance(res.exc, OSError)
    assert res.code != 0
    assert res.out == []
    assert res.stdout == ''
    assert res.err == []
    assert res.stderr == ''
