def test_is_repo_no_repo(initrepo):
    repo = initrepo(init=False)
    assert repo.is_repo is False


def test_is_repo_in_repo(initrepo):
    repo = initrepo(init=True)
    assert repo.is_repo is True
