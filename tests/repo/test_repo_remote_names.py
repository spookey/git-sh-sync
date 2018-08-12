from git_sh_sync.repo import Repository


def test_remote_names_empty(tmpdir):
    folder = tmpdir.join('repo.git')
    assert folder.stat(raising=False) is None

    repo = Repository(str(folder))
    assert repo.remote_names == []

    assert folder.remove() is None


def test_remote_names_clone(tmpdir, gitrepo):
    folder = tmpdir.join('repo.git')
    assert folder.stat(raising=False) is None

    repo = Repository(str(folder), remote_url=str(gitrepo.folder))
    assert repo.remote_name == 'origin'
    assert repo.remote_names == ['origin']

    assert folder.remove() is None


def test_remote_names_clone_named(tmpdir, gitrepo):
    folder = tmpdir.join('repo.git')
    assert folder.stat(raising=False) is None

    repo = Repository(
        str(folder),
        remote_url=str(gitrepo.folder),
        remote_name='test'
    )
    assert repo.remote_name == 'test'
    assert repo.remote_names == ['test']

    assert folder.remove() is None
