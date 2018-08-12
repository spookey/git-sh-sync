'''
This module allows working with git repositories.
'''
from collections import namedtuple
from logging import getLogger

from git_sh_sync.proc import Command
from git_sh_sync.util.disk import ensured
from git_sh_sync.util.host import get_hostname


class GitStatus(namedtuple('GitStatus', (
        'clean', 'conflicting', 'deleted', 'modified', 'untracked'
))):
    '''
    :arg clean: Is ``True`` if there are pending changes, otherwise ``False``
    :arg conflicting: Files with conflicts ``\\o/``
    :arg deleted: Removed files
    :arg modified: Files with modifications
    :arg untracked: Files not yet added end up here
    '''


class GitBranches(namedtuple('GitBranches', (
        'current', 'all'
))):
    '''
    :arg current: Currently active branch
    :arg all: All available branches (including *current*)
    '''


class Repository:
    '''
    Handles communications with git repositories, using native ``git``
    inside :class:`Command <git_sh_sync.proc.Command>`
    '''

    def __init__(
            self, location, *,
            master_branch='master', remote_name='origin', remote_url=None
    ):
        '''
        Initialize a new Repository

        :param location: Local path of the repository
        :param master_branch: Name of the master branch
        :param remote_name: Default name of the remote
        :param remote_url: Remote URL of the repository

        Calls then :meth:`initialize` to set everything up
        '''
        self._log = getLogger(self.__class__.__name__)

        self.location = ensured(location, folder=True)
        self.master_branch = master_branch.strip()
        self.remote_name = remote_name.strip()

        self.initialize(remote_url)

    @property
    def is_repo(self):
        '''
        Verifies if current :class:`Repository` is indeed a git repository.
        '''
        cmd = Command('git rev-parse --show-toplevel', cwd=self.location)
        return cmd() and cmd.stdout == self.location

    def initialize(self, remote_url=None):
        '''
        Is called from inside :meth:`__init__` to prepare the repository.
        Checks :attr:`is_repo` first to bail out early.
        If no *remote_url* is given a new repository is initialized.
        Otherwise a clone from the *remote_url* is attempted.
        '''
        if self.is_repo:
            return True

        if remote_url is not None:
            cmd = Command('git clone "{}" -o "{}" .'.format(
                remote_url, self.remote_name
            ), cwd=self.location)
            return cmd()

        cmd = Command('git init', cwd=self.location)
        return cmd()

    @property
    def status(self):
        '''
        Determines current status of the repository.

        :returns: Current status
        :rtype: :class:`GitStatus`

        Generates lists of changed files according to matching state.
        '''
        symbols = dict(
            conflicting='U', deleted='D', modified='M', untracked='?'
        )
        res = dict((key, []) for key in symbols)

        cmd = Command('git status --porcelain', cwd=self.location)
        if cmd():
            for elem in cmd.out:
                sym, obj = elem[:2].strip(), elem[3:].strip()
                for key, state in symbols.items():
                    if state in sym:
                        res[key].append(obj)

        return GitStatus(**res, clean=not any(res.values()))

    def branches(self):
        '''
        Collects all branches of the repository

        :returns: All branches
        :rtype: :class:`GitBranches`

        Signals current branch and a list of all other branches.
        '''
        res = dict(current=None, all=[])
        cmd = Command('git branch', cwd=self.location)
        if cmd():
            for elem in cmd.out:
                if '*' in elem:
                    elem = elem.replace('*', '')
                    res['current'] = elem.strip()
                res['all'].append(elem.strip())

        if res['current'] is None:
            cmd = Command('git symbolic-ref --short HEAD', cwd=self.location)
            if cmd():
                res['current'] = cmd.stdout
                res['all'].append(cmd.stdout)

        return GitBranches(**res)

    @property
    def remote_names(self):
        '''
        Emit names of the remotes.
        Do not confuse this property with the *remote_name*, which acts as
        a default value for cloning or pushing actions.

        :returns: Remote names
        :rtype: list
        '''
        cmd = Command('git remote show -n', cwd=self.location)
        cmd()
        return cmd.out

    def remote_url(self, remote=None):
        '''
        Retrieve URL of remote by name.

        :param remote: Remote name
        :returns: The URL as String or ``None`` if nothing was found
        '''
        if remote is None:
            remote = self.remote_name

        cmd = Command(
            'git remote get-url --push "{}"'.format(remote), cwd=self.location
        )
        if cmd():
            return cmd.stdout
        return None
