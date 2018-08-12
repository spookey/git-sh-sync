'''
This module handles communication with the operating system.
Namely launching commands.
'''

from logging import getLogger
from pprint import pformat
from shlex import quote, split
from subprocess import PIPE, Popen

from git_sh_sync.util.disk import joined

CODE_SUCCESS = 0
'''
Returncode of a successful command
'''


class Command:
    '''
    This is a class-based command runner using
    :py:mod:`subprocess`.
    '''

    def __init__(self, cmd, *, cwd=None, cin=None):
        '''
        Initialize a new command

        :param cmd: Commandline of command to launch
        :param cwd: Launch *cmd* inside some other current working directory
        :param cin: Send data via stdin into *cmd*
        '''
        if isinstance(cmd, str):
            cmd = split(cmd)

        if cwd is not None:
            cwd = joined(cwd)

        self._log = getLogger(self.__class__.__name__)
        self._data = dict(
            cmd=cmd, cwd=cwd, cin=cin,
            stdout='', stderr='', code=None, exc=None
        )

        self._log.debug('command initialized: """%s"""', str(self))

    @property
    def cmd(self):
        '''
        :returns: :py:func:`Splitted <shlex.split>` output of original *cmd*
        '''
        return self._data.get('cmd', [])

    @property
    def cwd(self):
        '''
        :returns: Current working directory or ``None``
        '''
        return self._data.get('cwd', None)

    @property
    def cin(self):
        '''
        :returns: Stdin data or ``None``
        '''
        return self._data.get('cin', None)

    @property
    def exc(self):
        '''
        :returns:
            If launching the command raised some exception it is
            available here, otherwise ``None``
        '''
        return self._data.get('exc', None)

    @property
    def code(self):
        '''
        :returns:
            The shell returncode after launching. Will be ``None``
            on exception or before launch
        '''
        return self._data.get('code', None)

    @property
    def stdout(self):
        '''
        :returns: Unmodified output of command stdout or empty string
        :rtype: str
        '''
        return self._data.get('stdout', '')

    @property
    def stderr(self):
        '''
        :returns: Unmodified output of command stderr or empty string
        :rtype: str
        '''
        return self._data.get('stderr', '')

    @property
    def command(self):
        '''
        :returns:
            Joined and :py:func:`quoted <shlex.quote>` output of internal
            :meth:`cmd`
        '''
        return ' '.join(quote(cmd) for cmd in self.cmd)

    @property
    def launched(self):
        '''
        :returns: ``True`` if command was launched, otherwise ``False``
        '''
        return self.exc is not None or self.code is not None

    @property
    def success(self):
        '''
        :returns:
            ``True`` if command launch was successful, otherwise ``False``

        A command is considered successful if no :func:`exception <exc>`
        was thrown and the :func:`returncode <code>` equals 0
        '''
        return self.exc is None and self.code == CODE_SUCCESS

    @property
    def out(self):
        '''
        :returns: Splitted list output of :meth:`stdout`
        :rtype: list
        '''
        return self.stdout.splitlines()

    @property
    def err(self):
        '''
        :returns: Splitted list output of :meth:`stderr`
        :rtype: list
        '''
        return self.stderr.splitlines()

    @property
    def fields(self):
        '''
        :returns: Some information about the current command as dictionary
        :rtype: dict

        Before the command was :meth:`launched <launched>` only
        :meth:`cmd`, :meth:`cwd` and :meth:`cin` are included.
        After :meth:`launch <launched>` the result is extended by
        :meth:`stdout`, :meth:`stderr`, :meth:`exc` and :meth:`code`.
        '''
        res = dict(command=self.command, cwd=self.cwd, cin=self.cin)
        if self.launched:
            res.update(
                stdout=self.stdout, stderr=self.stderr,
                exc=self.exc, code=self.code
            )
        return res

    def __repr__(self):
        '''
        String representation of current command.
        Utilizes :meth:`fields` and :py:func:`pprint.pformat` for that.
        '''
        return pformat(self.fields)

    def __call__(self):
        '''
        Launches the command.

        :returns: Output of :meth:`success`

        To avoid confusion a previously :meth:`launched <launched>` command
        will not run again, returning always ``False``.
        '''
        if self.launched:
            return False

        try:
            proc = Popen(
                self.cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                cwd=self.cwd, universal_newlines=True
            )
        except(OSError, TypeError, ValueError) as exc:
            self._data['exc'] = exc
        else:
            stdout, stderr = proc.communicate(input=self.cin)
            self._data['code'] = proc.returncode
            self._data['stdout'] = stdout.strip()
            self._data['stderr'] = stderr.strip()

        if self.success:
            self._log.info('command success: """%s"""', str(self))
        else:
            self._log.error('command failed: """%s"""', str(self))

        return self.success
