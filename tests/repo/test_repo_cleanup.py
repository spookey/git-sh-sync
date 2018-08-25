from logging import ERROR, WARNING

from git_sh_sync.repo import Repository


def test_cleanup_missing_remote(tmpdir):
    folder = tmpdir.join('repo.git')
    repo = Repository(str(folder))

    assert repo.status.clean is True
    assert repo.cleanup() is False

    assert folder.remove() is None


def test_cleanup_empty_remote(tmpdir, gitrepo):
    folder = tmpdir.join('repo.git')
    repo = Repository(str(folder), remote_url=str(gitrepo.folder))

    assert repo.status.clean is True
    assert repo.cleanup() is False

    assert folder.remove() is None


def test_cleanup_conflict_local(gitrepo, conflict, caplog):
    caplog.set_level(WARNING)
    assert not caplog.records

    assert gitrepo.repo.status.clean is True

    conflict(gitrepo)
    assert gitrepo.repo.status.clean is False

    assert gitrepo.repo.cleanup() is False

    assert len(caplog.records) >= 1

    rec = caplog.records[-1]
    assert rec.levelno == WARNING
    assert 'problems discovered' in rec.msg
    assert 'will not continue' in rec.msg


def test_cleanup_unrelated_remote(tmpdir, gitrepo):
    folder = tmpdir.join('repo.git')
    repo = Repository(str(folder), remote_url=str(gitrepo.folder))

    gitrepo.write('file', 'content_remote')
    gitrepo.add('file')
    gitrepo.commit('commit message')

    folder.join('file').write_text('content_local', 'utf-8', ensure=True)
    assert repo.scrub() is True

    assert repo.cleanup() is False

    assert folder.remove() is None


def test_cleanup_conflict_remote(tmpdir, gitrepo, caplog):
    caplog.set_level(ERROR)
    assert not caplog.records

    gitrepo.write('file', 'content')
    gitrepo.add('file')
    gitrepo.commit('first commit')

    folder = tmpdir.join('repo.git')
    repo = Repository(str(folder), remote_url=str(gitrepo.folder))

    gitrepo.write('file', 'remote_content')
    gitrepo.add('file')
    gitrepo.commit('remote commit')

    folder.join('file').write_text('content_local', 'utf-8', ensure=True)
    assert repo.scrub() is True

    assert repo.cleanup() is False

    assert len(caplog.records) >= 1

    rec = caplog.records[-1]
    assert rec.levelno == ERROR
    assert 'conflict detected' in rec.msg
    assert 'while pulling' in rec.msg

    assert folder.remove() is None


def test_cleanup_pulls_into_empty(tmpdir, gitrepo):
    folder = tmpdir.join('repo.git')
    repo = Repository(str(folder), remote_url=str(gitrepo.folder))

    gitrepo.write('file', 'content')
    gitrepo.add('file')
    gitrepo.commit('first commit')

    assert folder.join('file').stat(raising=False) is None

    assert repo.cleanup() is True

    log = repo.log()
    assert len(log) == 1
    assert 'first commit' in log[0].message

    assert folder.join('file').stat(raising=False) is not None

    assert folder.remove() is None


def test_cleanup_merges(tmpdir, gitrepo):
    gitrepo.write('file', 'initial content')
    gitrepo.add('file')
    gitrepo.commit('first commit')

    folder = tmpdir.join('repo.git')
    assert folder.join('file').stat(raising=False) is None

    repo = Repository(str(folder), remote_url=str(gitrepo.folder))
    assert folder.join('file').stat(raising=False) is not None

    gitrepo.write('file', 'changed content')
    gitrepo.add('file')
    gitrepo.commit('remote commit')

    folder.join('file').write_text('changed content', 'utf-8')

    assert repo.status.clean is False
    assert repo.cleanup() is True

    log = repo.log()
    assert len(log) == 4

    assert 'first commit' in log[-1].message
    assert 'remote commit' in log[-2].message
    assert 'auto commit' in log[-3].message
    assert 'merge branch' in log[-4].message.lower()

    assert folder.remove() is None
