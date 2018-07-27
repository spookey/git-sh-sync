from logging import getLogger
from pprint import pformat
from shlex import quote, split
from subprocess import PIPE, Popen


class Command:
    def __init__(self, cmd, *, cwd=None, cin=None):
        if isinstance(cmd, str):
            cmd = split(cmd)

        self._log = getLogger(self.__class__.__name__)
        self._data = dict(
            cmd=cmd, cwd=cwd, cin=cin,
            stdout='', stderr='', code=None, exc=None
        )

        self._log.debug('command initialized: """%s"""', str(self))

    @property
    def cmd(self):
        return self._data.get('cmd', [])

    @property
    def cwd(self):
        return self._data.get('cwd', None)

    @property
    def cin(self):
        return self._data.get('cin', None)

    @property
    def exc(self):
        return self._data.get('exc', None)

    @property
    def code(self):
        return self._data.get('code', None)

    @property
    def stdout(self):
        return self._data.get('stdout', '')

    @property
    def stderr(self):
        return self._data.get('stderr', '')

    @property
    def command(self):
        return ' '.join(quote(cmd) for cmd in self.cmd)

    @property
    def launched(self):
        return self.exc is not None or self.code is not None

    @property
    def success(self):
        return self.exc is None and self.code == 0

    @property
    def out(self):
        return self.stdout.splitlines()

    @property
    def err(self):
        return self.stderr.splitlines()

    @property
    def _fields(self):
        res = dict(command=self.command, cwd=self.cwd, cin=self.cin)
        if self.launched:
            res.update(
                stdout=self.stdout, stderr=self.stderr,
                exc=self.exc, code=self.code
            )
        return res

    def __repr__(self):
        return pformat(self._fields)

    def __call__(self):
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
