def test_status_untracked(gitrepo):
    assert gitrepo.repo.status.untracked == []
    assert gitrepo.repo.status.clean is True

    gitrepo.write('untracked', '')

    assert gitrepo.repo.status.untracked == ['untracked']
    assert gitrepo.repo.status.clean is False


def test_status_modified(gitrepo):
    assert gitrepo.repo.status.modified == []
    assert gitrepo.repo.status.clean is True

    gitrepo.write('modified', 'aaa')

    assert gitrepo.repo.status.modified == []
    assert gitrepo.repo.status.clean is False

    gitrepo.add('modified')

    assert gitrepo.repo.status.modified == []
    assert gitrepo.repo.status.clean is True

    gitrepo.write('modified', 'bbb')

    assert gitrepo.repo.status.modified == ['modified']
    assert gitrepo.repo.status.clean is False


def test_status_deleted(gitrepo):
    assert gitrepo.repo.status.deleted == []
    assert gitrepo.repo.status.clean is True

    gitrepo.write('deleted', '')

    assert gitrepo.repo.status.deleted == []
    assert gitrepo.repo.status.clean is False

    gitrepo.add('deleted')
    gitrepo.commit('delete file')

    assert gitrepo.repo.status.deleted == []
    assert gitrepo.repo.status.clean is True

    gitrepo.rm('deleted')

    assert gitrepo.repo.status.deleted == ['deleted']
    assert gitrepo.repo.status.clean is False


def test_status_conflicting(gitrepo, conflict):
    assert gitrepo.repo.status.conflicting == []
    assert gitrepo.repo.status.clean is True

    conflict(gitrepo, 'conflicting')

    assert gitrepo.repo.status.conflicting == ['conflicting']
    assert gitrepo.repo.status.clean is False
