from collections import namedtuple
from logging import getLogger
from subprocess import run

from pytest import fixture

from git_sh_sync.repo import Repository


@fixture(scope='function')
def initrepo(tmpdir, monkeypatch):
    folder = tmpdir.mkdir('initrepo.git')
    repo = Repository

    def init(_, *, init):
        setattr(repo, 'folder', folder)

        setattr(repo, 'location', str(folder))
        setattr(repo, 'remote_name', 'origin')
        setattr(repo, '_log', getLogger(repo.__class__.__name__))

        if init:
            run(['git', 'init'], cwd=str(folder))

    monkeypatch.setattr(repo, '__init__', init)

    yield repo

    assert folder.remove() is None


@fixture(scope='function')
def gitrepo(tmpdir):
    folder = tmpdir.mkdir('gitrepo.git')
    repo = Repository(location=str(folder))

    yield namedtuple('GitRepo', (
        'repo', 'folder', 'write', 'remove',
        'add', 'commit', 'rm', 'checkout_branch', 'checkout', 'merge', 'tag',
        'make_bare'
    ))(
        repo=repo, folder=folder,
        write=lambda name, text: folder.join(name).write_text(
            text, 'utf-8', ensure=True
        ),
        remove=lambda name: folder.join(name).remove(),
        add=lambda *files: run(
            ['git', 'add', *files], cwd=repo.location
        ),
        commit=lambda msg: run(
            ['git', 'commit', '-m', '{}'.format(msg)], cwd=repo.location
        ),
        rm=lambda *files: run(
            ['git', 'rm', *files], cwd=repo.location
        ),
        checkout_branch=lambda name: run(
            ['git', 'checkout', '-b', name], cwd=repo.location
        ),
        checkout=lambda name: run(
            ['git', 'checkout', name], cwd=repo.location
        ),
        merge=lambda name: run(
            ['git', 'merge', name], cwd=repo.location
        ),
        tag=lambda name: run(
            ['git', 'tag', name], cwd=repo.location
        ),
        make_bare=lambda: run(
            ['git', 'config', '--bool', 'core.bare', 'true'], cwd=repo.location
        ),
    )

    assert folder.remove() is None


@fixture(scope='function')
def conflict():
    def make(gtrp, filename='file', brc_org='master', brc_sec='temp'):
        assert gtrp.repo.status.clean is True
        gtrp.checkout_branch(brc_org)

        gtrp.write(filename, 'content 1')
        gtrp.add(filename)
        gtrp.commit('commit 1')

        assert gtrp.repo.status.clean is True
        gtrp.checkout_branch(brc_sec)

        gtrp.write(filename, 'content 2')
        gtrp.add(filename)
        gtrp.commit('commit 2')

        assert gtrp.repo.status.clean is True
        gtrp.checkout(brc_org)

        gtrp.write(filename, 'content 3')
        gtrp.add(filename)
        gtrp.commit('commit 3')

        assert gtrp.repo.status.clean is True
        gtrp.merge(brc_sec)

        assert gtrp.repo.status.clean is False

    yield make
