def test_log_empty(gitrepo):
    assert gitrepo.repo.log() == []


def test_log_single(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    logs = gitrepo.repo.log()
    assert len(logs) == 1

    log = logs[-1]
    assert log.full.startswith(log.short)
    assert log.message == 'aaa commit message'


def test_log_multi(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    gitrepo.write('bbb', 'content')
    gitrepo.add('bbb')
    gitrepo.commit('bbb commit message')

    logs = gitrepo.repo.log()
    assert len(logs) == 2

    logs = gitrepo.repo.log(num=1)
    assert len(logs) == 1

    log = logs[-1]
    assert log.full.startswith(log.short)
    assert log.message == 'bbb commit message'
