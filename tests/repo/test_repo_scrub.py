from logging import ERROR, WARNING


def test_scrub_empty(gitrepo):
    assert gitrepo.repo.status.clean is True
    assert gitrepo.repo.scrub() is True


def test_scrub_conflict(gitrepo, conflict, caplog):
    caplog.set_level(WARNING)
    assert not caplog.records

    assert gitrepo.repo.status.clean is True

    conflict(gitrepo, filename='file')
    assert gitrepo.repo.scrub() is False

    assert len(caplog.records) >= 2

    rec = caplog.records[-2]
    assert rec.levelno == ERROR
    assert 'conflicting file' in rec.msg
    assert 'file' in rec.args[0]

    rec = caplog.records[-1]
    assert rec.levelno == WARNING
    assert 'problems discovered' in rec.msg
    assert 'will not continue' in rec.msg


def test_scrub_commits(gitrepo):
    assert gitrepo.repo.status.clean is True
    assert gitrepo.repo.log() == []

    gitrepo.write('file', 'content')

    status = gitrepo.repo.status
    assert status.clean is False
    assert 'file' in status.untracked

    assert gitrepo.repo.scrub() is True

    log = gitrepo.repo.log()
    assert len(log) == 1

    assert 'auto commit' in log[-1].message
