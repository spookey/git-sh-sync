from collections import namedtuple
from subprocess import run

from pytest import fixture

from git_sh_sync.repo import Repository


@fixture(scope='function')
def initrepo(tmpdir, monkeypatch):
    folder = tmpdir.mkdir('initrepo.git')
    repo = Repository

    def init(_, *, init):
        repo.location = str(folder)
        repo.remote_name = 'origin'
        if init:
            run(['git', 'init'], cwd=repo.location)
        repo.folder = folder

    monkeypatch.setattr(Repository, '__init__', init)

    yield repo

    assert folder.remove() is None


@fixture(scope='function')
def gitrepo(tmpdir):
    folder = tmpdir.mkdir('gitrepo.git')
    repo = Repository(location=str(folder))

    yield namedtuple('GitRepo', (
        'repo', 'folder', 'write',
        'add', 'commit', 'rm', 'checkout_branch', 'checkout', 'merge'
    ))(
        repo=repo, folder=folder,
        write=lambda name, text: folder.join(name).write_text(
            text, 'utf-8', ensure=True
        ),
        add=lambda *files: run(
            ['git', 'add', *files], cwd=repo.location
        ),
        commit=lambda msg: run(
            ['git', 'commit', '-m', '"{}"'.format(msg)], cwd=repo.location
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
    )

    assert folder.remove() is None
