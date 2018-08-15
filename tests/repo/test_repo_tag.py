def test_tag_onto_empty(gitrepo):
    assert gitrepo.repo.tag('test') is False


def test_tag_create(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    assert gitrepo.repo.tag('aaa-tag') is True

    assert gitrepo.repo.tags == ['aaa-tag']

    gitrepo.write('bbb', 'content')
    gitrepo.add('bbb')
    gitrepo.commit('bbb commit message')

    assert gitrepo.repo.tag('bbb-tag') is True

    assert gitrepo.repo.tags == ['bbb-tag', 'aaa-tag']


def test_tag_same(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    assert gitrepo.repo.tag('test') is True

    assert gitrepo.repo.tags == ['test']

    gitrepo.write('bbb', 'content')
    gitrepo.add('bbb')
    gitrepo.commit('bbb commit message')

    assert gitrepo.repo.tag('test') is False

    assert gitrepo.repo.tags == ['test']
