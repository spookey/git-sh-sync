def test_checkout_branch_empty(gitrepo):
    brc = gitrepo.repo.branches()
    assert brc.current == 'master'
    assert brc.all == ['master']

    assert gitrepo.repo.checkout('test') is True

    brc = gitrepo.repo.branches()
    assert brc.current == 'test'
    assert brc.all == ['test']


def test_checkout_tag(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    gitrepo.tag('aaa-tag')

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None

    gitrepo.write('bbb', 'content')
    gitrepo.add('bbb')
    gitrepo.commit('bbb commit message')

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None
    assert gitrepo.folder.join('bbb').stat(raising=False) is not None

    assert gitrepo.repo.checkout('aaa-tag')

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None
    assert gitrepo.folder.join('bbb').stat(raising=False) is None


def test_checkout_commit(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    back_log = gitrepo.repo.log()

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None

    gitrepo.write('bbb', 'content')
    gitrepo.add('bbb')
    gitrepo.commit('bbb commit message')

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None
    assert gitrepo.folder.join('bbb').stat(raising=False) is not None

    assert gitrepo.repo.checkout(back_log[-1].short)

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None
    assert gitrepo.folder.join('bbb').stat(raising=False) is None

    assert gitrepo.repo.checkout(back_log[-1].full)

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None
    assert gitrepo.folder.join('bbb').stat(raising=False) is None


def test_checkout_master(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None

    assert gitrepo.repo.checkout('test') is True

    gitrepo.write('bbb', 'content')
    gitrepo.add('bbb')
    gitrepo.commit('bbb commit message')

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None
    assert gitrepo.folder.join('bbb').stat(raising=False) is not None

    assert gitrepo.repo.checkout() is True

    assert gitrepo.folder.join('aaa').stat(raising=False) is not None
    assert gitrepo.folder.join('bbb').stat(raising=False) is None
