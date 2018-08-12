from git_sh_sync.repo import Repository


def test_repo_init_creates(tmpdir):
    folder = tmpdir.join('repo.git')
    assert folder.stat(raising=False) is None

    g_folder = folder.join('.git')
    assert g_folder.stat(raising=False) is None

    repo = Repository(str(folder))
    assert repo.location == str(folder)

    assert folder.stat(raising=False) is not None
    assert g_folder.stat(raising=False) is not None

    assert folder.remove() is None


def test_repo_init_clones(tmpdir, gitrepo):
    folder = tmpdir.join('repo.git')
    assert folder.stat(raising=False) is None

    g_folder = folder.join('.git')
    assert g_folder.stat(raising=False) is None

    assert gitrepo.folder.stat(raising=False) is not None

    repo = Repository(str(folder), remote_url=str(gitrepo.folder))
    assert repo.location == str(folder)

    assert folder.stat(raising=False) is not None
    assert g_folder.stat(raising=False) is not None

    assert folder.remove() is None
