def test_tags_empty(gitrepo):
    assert gitrepo.repo.tags == []


def test_tags_single(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    gitrepo.tag('aaa-tag')

    tags = gitrepo.repo.tags
    assert len(tags) == 1

    tag = tags[-1]
    assert tag == 'aaa-tag'


def test_tags_multi(gitrepo):
    gitrepo.write('aaa', 'content')
    gitrepo.add('aaa')
    gitrepo.commit('aaa commit message')

    gitrepo.tag('aaa-tag')

    gitrepo.write('bbb', 'content')
    gitrepo.add('bbb')
    gitrepo.commit('bbb commit message')

    gitrepo.tag('bbb-tag')

    tags = gitrepo.repo.tags
    assert len(tags) == 2

    assert tags[0] == 'bbb-tag'
    assert tags[1] == 'aaa-tag'
