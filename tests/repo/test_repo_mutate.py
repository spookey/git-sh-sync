from logging import ERROR


def test_mutate_empty(gitrepo):
    assert gitrepo.repo.mutate() is True


def test_mutate_addition(gitrepo):
    assert gitrepo.repo.status.clean is True

    gitrepo.write('file', 'content')

    status = gitrepo.repo.status
    assert status.clean is False
    assert 'file' in status.untracked

    assert gitrepo.repo.mutate() is True
    assert gitrepo.repo.status.clean is True


def test_mutate_modification(gitrepo):
    assert gitrepo.repo.status.clean is True

    gitrepo.write('file', 'content_1')

    assert gitrepo.repo.status.clean is False

    assert gitrepo.repo.mutate() is True
    assert gitrepo.repo.status.clean is True

    gitrepo.write('file', 'content_2')

    status = gitrepo.repo.status
    assert status.clean is False
    assert 'file' in status.modified

    assert gitrepo.repo.mutate() is True
    assert gitrepo.repo.status.clean is True


def test_mutate_deletion(gitrepo):
    assert gitrepo.repo.status.clean is True

    gitrepo.write('file', 'content')

    assert gitrepo.repo.status.clean is False

    assert gitrepo.repo.mutate() is True
    assert gitrepo.repo.status.clean is True

    gitrepo.remove('file')

    status = gitrepo.repo.status
    assert status.clean is False
    assert 'file' in status.deleted

    assert gitrepo.repo.mutate() is True
    assert gitrepo.repo.status.clean is True


def test_mutate_conflict_org(gitrepo, conflict):
    conflict(gitrepo)

    assert gitrepo.repo.mutate() is False

    status = gitrepo.repo.status
    assert status.clean is False
    assert 'file' in status.conflicting


def test_mutate_conflict_logs(gitrepo, conflict, caplog):
    caplog.set_level(ERROR)
    assert not caplog.records

    conflict(gitrepo)

    assert gitrepo.repo.mutate() is False
    assert gitrepo.repo.status.clean is False

    assert len(caplog.records) == 1

    rec = caplog.records[-1]
    assert rec.levelno == ERROR
    assert 'conflicting file' in rec.msg
    assert 'file' in rec.args[0]
    assert gitrepo.repo.location in rec.args[-1]
