def test_initialize_works(initrepo):
    repo = initrepo(init=False)
    git_dir = repo.folder.join('.git')
    assert git_dir.stat(raising=False) is None

    assert repo.initialize()

    assert git_dir.stat(raising=False) is not None


def test_initialize_skips(initrepo):
    repo = initrepo(init=True)
    git_dir = repo.folder.join('.git')
    assert git_dir.stat(raising=False) is not None

    assert repo.initialize()

    assert git_dir.stat(raising=False) is not None


def test_initialize_clones(gitrepo, initrepo):
    repo = initrepo(init=False)
    git_dir = repo.folder.join('.git')
    assert git_dir.stat(raising=False) is None

    assert gitrepo.folder.stat(raising=False) is not None

    assert repo.initialize(remote_url=str(gitrepo.folder))

    assert git_dir.stat(raising=False) is not None
