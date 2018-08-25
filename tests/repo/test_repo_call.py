from git_sh_sync.repo import Repository


def test_call_missing_remote(tmpdir):
    folder = tmpdir.join('repo.git')
    repo = Repository(str(folder))

    assert repo() is False

    assert folder.remove() is None


def test_call_complete_cycle(tmpdir, gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa')

    gitrepo.make_bare()

    folder = tmpdir.join('repo.git')
    repo = Repository(str(folder), remote_url=str(gitrepo.folder))

    folder.join('bbb').write_text('content', 'utf-8')

    assert gitrepo.repo.status.clean is True
    assert repo.status.clean is False

    assert repo() is True

    assert gitrepo.repo.status.clean is True
    assert repo.status.clean is True

    assert folder.remove() is None
