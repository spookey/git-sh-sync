def test_branches_empty(gitrepo):
    branches = gitrepo.repo.branches()
    assert branches.current == 'master'
    assert branches.all == ['master']


def test_branch_switch(gitrepo):
    branches = gitrepo.repo.branches()
    assert branches.current == 'master'
    assert branches.all == ['master']

    gitrepo.checkout_branch('client')

    branches = gitrepo.repo.branches()
    assert branches.current == 'client'
    assert branches.all == ['client']


def test_branch_empty_switch(gitrepo):
    branches = gitrepo.repo.branches()
    assert branches.current == 'master'
    assert branches.all == ['master']

    gitrepo.checkout_branch('client')

    gitrepo.write('xyz', 'xyz')
    gitrepo.add('xyz')
    gitrepo.commit('xyz')

    branches = gitrepo.repo.branches()
    assert branches.current == 'client'
    assert branches.all == ['client']


def test_branch_dual_switch(gitrepo):
    branches = gitrepo.repo.branches()
    assert branches.current == 'master'
    assert branches.all == ['master']

    gitrepo.write('abc', 'abc')
    gitrepo.add('abc')
    gitrepo.commit('abc')

    gitrepo.checkout_branch('client')

    gitrepo.write('xyz', 'xyz')
    gitrepo.add('xyz')
    gitrepo.commit('xyz')

    branches = gitrepo.repo.branches()
    assert branches.current == 'client'
    assert branches.all == ['client', 'master']
