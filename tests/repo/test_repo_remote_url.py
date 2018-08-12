from git_sh_sync.repo import Repository


def test_remote_url_empty(tmpdir):
    folder = tmpdir.join('repo.git')
    assert folder.stat(raising=False) is None

    repo = Repository(str(folder))
    assert repo.remote_url() is None

    assert folder.remove() is None


def test_remote_url_clone(tmpdir, gitrepo):
    folder = tmpdir.join('repo.git')
    assert folder.stat(raising=False) is None

    repo = Repository(str(folder), remote_url=str(gitrepo.folder))
    assert repo.remote_names == ['origin']

    assert repo.remote_url() == str(gitrepo.folder)

    assert folder.remove() is None
