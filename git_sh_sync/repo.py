'''
This module allows working with git repositories.
'''
from collections import namedtuple
from logging import getLogger

from git_sh_sync.proc import Command
from git_sh_sync.util.disk import ensured

GIT_DIVIDER = '|-: ^_^ :-|'
'''
Format divider (e.g. used in log) - Should be different from any text
inside a commit message
'''


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


class GitLog(namedtuple('GitLog', (
        'short', 'full', 'message'
))):
    '''
    :arg short: Short commit hash
    :arg full: Complete commit hash
    :arg message: Commit message
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

        if self.initialize(remote_url):
            self.checkout()

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

    def log(self, num=-1):
        '''
        Retrieve log of repository

        :param num: Limit length of output. Use negative for unlimited output.
        :returns: Log entries containing short-, full-hash and commit message.
        :rtype: list of :class:`GitLog`
        '''
        result = []
        cmd = Command('git log --max-count {} --format="{}"'.format(
            num, GIT_DIVIDER.join(['%h', '%H', '%B'])
        ), cwd=self.location)
        if cmd():
            for elem in (el for el in cmd.out if el):
                short, full, message = elem.split(GIT_DIVIDER)
                result.append(GitLog(short=short, full=full, message=message))
        return result

    @property
    def tags(self):
        '''
        Query existing tags.

        :returns: Name of tags, newest first
        :rtype: list
        '''
        cmd = Command(
            'git tag --list --sort="-version:refname"',
            cwd=self.location
        )
        cmd()
        return cmd.out

    def tag(self, name):
        '''
        Stick tags onto commits.

        :param name: Tag name
        :returns: ``True`` if successful else ``False``
        '''
        cmd = Command('git tag "{}"'.format(name), cwd=self.location)
        return cmd()

    def checkout(self, treeish=None):
        '''
        Checkout a commit, tag or branch.

        :param treeish: Commit (short or full), tag or branch.
                        If left blank, *master_branch* is assumed
        :returns: ``True`` if successful else ``False``

        If *treeish* is neither a known commit, tag or branch, a new branch
        is created.
        '''
        if treeish is None:
            treeish = self.master_branch

        def is_known():
            '''
            Helper to optimize detection if *treeish* is a known
            tag, branch or commit.
            '''
            if treeish in self.tags:
                return True

            branches = self.branches()
            for branch in branches.all:
                if treeish in branch:
                    return True

            for log in self.log():
                if treeish in log.short:
                    return True
                if treeish in log.full:
                    return True
            return False

        line = (
            'git checkout "{}"' if is_known() else 'git checkout -b "{}"'
        ).format(treeish)

        cmd = Command(line, cwd=self.location)
        return cmd()

    def mutate(self):
        '''
        Collects all changes and tries to add/remove them.

        :returns: ``True`` if everything went well, else ``False``

        Will freak out if there are conflicts detected
        - thus returning ``False`` and writing issues into the log.
        '''
        status = self.status

        if status.clean:
            return True

        results = []

        def add(elem):
            cmd = Command('git add {}'.format(elem), cwd=self.location)
            return cmd()

        def remove(elem):
            cmd = Command('git rm {}'.format(elem), cwd=self.location)
            return cmd()

        for elem in status.untracked:
            results.append(add(elem))
        for elem in status.modified:
            results.append(add(elem))
        for elem in status.deleted:
            results.append(remove(elem))
        for elem in status.conflicting:
            self._log.error(
                'conflicting file "%s" discovered in "%s"',
                elem, self.location
            )
            results.append(False)

        return all(results)
